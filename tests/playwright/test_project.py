"""End-to-end checks for the rendered project pages (templates/project.html).

Drives a real browser against the site built from data.json and checks every
project's page. Optional sections (highlights, gallery, facts, technology
layer/purpose) are expected exactly when that project's data has them.
Expected values come from data.json itself (the site_data fixture), never
literals. See docs/arch/0019, 0033.
"""

import pytest


def _project_url(site_url, project):
    """Build the URL of one project's page.

    Args:
        site_url: Base URL of the served site.
        project: A project entry from data.json.

    Returns:
        str: URL of dist/projects/<project_name>/index.html.
    """
    return f"{site_url}/projects/{project['project_name']}/index.html"


def test_every_project_page_renders_its_sections(page, site_url, site_data):
    """Each page shows its title and exactly the sections its data calls for."""
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    name = site_data["profile"]["name"]

    for project in site_data["projects"]:
        page.goto(_project_url(site_url, project))

        assert page.title() == f"{project['title']} — {name}"
        assert page.locator(".project-title").inner_text() == project["title"]
        assert page.locator(".project-subtitle").inner_text() == project["tagline"]
        assert page.locator("section#background").is_visible()
        assert page.locator("section#preview").is_visible()
        for section, field in [
            ("highlights", "highlights"),
            ("technologies", "technologies"),
            ("gallery", "gallery"),
        ]:
            expected = 1 if project.get(field) else 0
            assert page.locator(f"section#{section}").count() == expected, (
                f"{project['project_name']}: #{section}"
            )
        paragraphs = project["description"].split("\n\n")
        assert page.locator("#background p").count() == len(paragraphs)

    assert errors == []


def test_project_links_render_as_buttons(page, site_url, site_data):
    """Each entry in a project's links becomes a button under the title."""
    for project in site_data["projects"]:
        page.goto(_project_url(site_url, project))
        buttons = page.locator(".project-actions a")

        assert buttons.count() == len(project["links"])
        for button, link in zip(buttons.all(), project["links"], strict=True):
            assert link["label"] in button.inner_text()
            href = button.get_attribute("href")
            if link["type"] == "download":
                assert href == f"../../{link['url']}"
            else:
                assert href == link["url"]


def test_technologies_show_as_table_or_logo_grid(page, site_url, site_data):
    """Featured techs get the large grid; the rest a table only when needed."""
    for project in site_data["projects"]:
        techs = project["technologies"]
        if not techs:
            continue
        page.goto(_project_url(site_url, project))
        featured = [tech for tech in techs if tech.get("featured")]
        others = [tech for tech in techs if not tech.get("featured")]
        has_layer = any(tech.get("layer") for tech in others)
        has_purpose = any(tech.get("purpose") for tech in others)

        assert page.locator("#technologies .tech-grid-featured li").count() == len(
            featured
        )
        expected_subheading = 1 if featured and others else 0
        assert page.locator("#technologies .tech-subheading").count() == (
            expected_subheading
        )
        if not others:
            assert page.locator("#technologies table").count() == 0
        elif has_layer or has_purpose:
            expected = (
                (["Layer"] if has_layer else [])
                + ["Technology"]
                + (["Purpose"] if has_purpose else [])
            )
            assert page.locator("#technologies th").all_text_contents() == expected
            assert page.locator("#technologies tbody tr").count() == len(others)
        else:
            plain_grid = "#technologies .tech-grid:not(.tech-grid-featured) li"
            assert page.locator(plain_grid).count() == len(others)


def test_also_used_technologies_expand_on_click(page, site_url, site_data):
    """Behind featured techs, the rest start collapsed and open on click."""
    projects = [
        p
        for p in site_data["projects"]
        if any(t.get("featured") for t in p["technologies"])
        and not all(t.get("featured") for t in p["technologies"])
    ]
    if not projects:
        pytest.skip("no project in data.json mixes featured and other technologies")
    project = projects[0]
    page.goto(_project_url(site_url, project))
    first_other = next(t for t in project["technologies"] if not t.get("featured"))
    row = page.locator("#technologies .tech-more").get_by_text(first_other["name"])

    assert not row.is_visible()
    page.locator("#technologies .tech-more summary").click()
    assert row.is_visible()


def test_highlights_beyond_three_expand_on_click(page, site_url, site_data):
    """The first three highlights show; the rest open from More highlights."""
    for project in site_data["projects"]:
        highlights = project.get("highlights") or []
        if not highlights:
            continue
        page.goto(_project_url(site_url, project))
        more = page.locator("#highlights .highlights-more")

        if len(highlights) <= 3:
            assert more.count() == 0
            continue
        hidden = more.locator("li")
        assert hidden.count() == len(highlights) - 3
        assert not hidden.first.is_visible()
        more.locator("summary").click()
        assert hidden.first.is_visible()


def test_preview_opens_and_closes_lightbox(page, site_url, site_data):
    """Clicking the main preview shows it full size; Close hides it again."""
    if not site_data["projects"]:
        pytest.skip("data.json has no projects")
    page.goto(_project_url(site_url, site_data["projects"][0]))
    lightbox = page.locator("#shot-1")

    assert not lightbox.is_visible()
    page.locator(".preview-frame").click()
    assert lightbox.is_visible()

    lightbox.locator(".lightbox-close").click()
    assert not lightbox.is_visible()


def test_gallery_thumbnail_opens_its_lightbox(page, site_url, site_data):
    """A gallery thumbnail opens the lightbox for that image, with its caption."""
    with_gallery = [p for p in site_data["projects"] if p.get("gallery")]
    if not with_gallery:
        pytest.skip("no project in data.json has a gallery")
    project = with_gallery[0]
    page.goto(_project_url(site_url, project))
    lightbox = page.locator("#shot-2")

    page.locator(".gallery-strip a").first.click()
    assert lightbox.is_visible()
    caption = project["gallery"][0].get("caption")
    if caption:
        assert caption in lightbox.inner_text()


def test_sidebar_marks_current_project(page, site_url, site_data):
    """All Projects lists every project and marks the current one."""
    projects = site_data["projects"]
    for project in projects:
        page.goto(_project_url(site_url, project))
        nav = page.locator(".project-nav-list")

        assert nav.locator("li").count() == len(projects)
        assert nav.locator("[aria-current='page']").inner_text() == project["title"]
