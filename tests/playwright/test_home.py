"""End-to-end checks for the rendered home page (templates/home.html).

Drives a real browser against the site built from data.json, so it catches
things unit tests can't: the theme toggle actually flips data-theme and
persists via localStorage, content from data.json actually renders, and the
page loads without console errors. Expected values come from data.json
itself (the site_data fixture), never literals. See docs/arch/0019, 0033.
"""

import pytest


def _js_exceptions(page):
    """Collect uncaught JS exceptions raised while page is used.

    Deliberately doesn't look at console "error" messages, which also
    include asset 404s; a missing image is a data.json problem, not a broken
    page. This only tracks actual script exceptions.

    Args:
        page: Playwright Page to attach the listener to.

    Returns:
        list[str]: Exception message texts, appended to as they occur.
    """
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    return errors


def _tel(phone):
    """Strip a display phone number down to its tel: form, like home.html does.

    Args:
        phone: Phone number as written in data.json, e.g. "(555) 555-5555".

    Returns:
        str: The digits-only form used in the tel: href.
    """
    for char in " ()-":
        phone = phone.replace(char, "")
    return phone


def test_home_page_loads_in_dark_theme_by_default(page, site_url, site_data):
    """With no stored preference, the page loads in dark mode."""
    profile = site_data["profile"]
    page.goto(site_url)

    assert page.title() == f"{profile['name']} — {profile['role']}"
    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert page.locator(".site-name").inner_text() == profile["name"]


def test_top_nav_links_to_real_pages(page, site_url):
    """Home/Projects in the header nav are real page links, not anchors."""
    page.goto(site_url)
    top_nav = page.locator(".site-header .site-nav")

    assert top_nav.get_by_role("link", name="Home").get_attribute("href") == (
        "index.html"
    )
    assert top_nav.get_by_role("link", name="Projects").get_attribute("href") == (
        "projects/index.html"
    )


def test_sidebar_quick_nav_and_sections_render(page, site_url):
    """The sidebar's in-page anchors and every section they point to exist."""
    page.goto(site_url)
    quick_nav = page.locator(".sidebar .nav-list")

    for label in [
        "About Me",
        "Skills",
        "Featured",
        "Resume",
        "Links",
        "Contact",
    ]:
        quick_nav.get_by_role("link", name=label).click()

    for anchor_id in [
        "about",
        "skills",
        "projects",
        "resume",
        "links",
        "contact",
    ]:
        assert page.locator(f"#{anchor_id}").count() == 1


def test_featured_projects_and_skills_render(page, site_url, site_data):
    """Every featured project and every skill from data.json shows up."""
    page.goto(site_url)
    featured = page.locator("#projects")
    skills = page.locator(".skills-table").inner_text()

    for project in site_data["projects"]:
        link = featured.get_by_role("link", name=project["title"], exact=True)
        assert link.count() == (1 if project.get("featured") else 0)
    for row in site_data["profile"]["skills"]:
        assert row["category"] in skills
        for tech in row["technologies"]:
            assert tech["name"] in skills


def test_contact_section_shows_phone(page, site_url, site_data):
    """profile.phone renders as a tel: link in the Contact section."""
    phone_number = site_data["profile"].get("phone")
    if not phone_number:
        pytest.skip("data.json has no profile.phone")
    page.goto(site_url)

    phone = page.locator("#contact").get_by_role("link", name=phone_number)
    assert phone.get_attribute("href") == f"tel:{_tel(phone_number)}"


def test_quick_info_shows_email_and_phone_under_contact(page, site_url, site_data):
    """Quick Info groups email and phone under one Contact label."""
    profile = site_data["profile"]
    page.goto(site_url)
    quick_info = page.locator(
        ".box", has=page.get_by_role("heading", name="Quick Info")
    )

    assert "Contact:" in quick_info.inner_text()
    assert quick_info.get_by_role("link", name=profile["email"]).is_visible()
    if profile.get("phone"):
        phone = quick_info.get_by_role("link", name=profile["phone"])
        assert phone.get_attribute("href") == f"tel:{_tel(profile['phone'])}"


def test_each_section_shows_its_own_header_quote(page, site_url, site_data):
    """Home and Projects pull different quotes from data.json's quotes."""
    quotes = site_data["quotes"]
    page.goto(site_url)
    assert quotes["home"] in page.locator(".site-quote").inner_text()

    page.goto(f"{site_url}/projects/index.html")
    assert quotes["projects"] in page.locator(".site-quote").inner_text()


def test_projects_index_has_featured_and_catalog_cards(page, site_url, site_data):
    """The project index shows image-led featured and catalog views."""
    projects = site_data["projects"]
    featured = [project for project in projects if project.get("featured")]
    page.goto(f"{site_url}/projects/index.html")

    assert page.title() == f"Projects — {site_data['profile']['name']}"
    for project in featured:
        assert (
            page.locator("#featured-projects")
            .get_by_role("link", name=project["title"], exact=True)
            .is_visible()
        )
    assert page.locator(".project-catalog .project-card").count() == len(projects)
    # Descriptions are featured-only; catalog cards show just the tagline.
    assert page.locator(".featured-project-copy > p:not([class])").count() == len(
        featured
    )
    assert page.locator(".project-card-copy > p:not([class])").count() == 0
    if projects:
        assert page.locator(".project-card-image img").first.get_attribute("src") == (
            f"../{projects[0]['image']}"
        )


def test_theme_toggle_switches_and_persists_after_reload(page, site_url):
    """Clicking the toggle flips the theme and localStorage survives a reload."""
    page.goto(site_url)
    toggle = page.locator("#theme-toggle")

    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert toggle.inner_text() == "Light Mode"

    toggle.click()

    assert page.locator("html").get_attribute("data-theme") == "light"
    assert toggle.inner_text() == "Dark Mode"
    assert toggle.get_attribute("aria-pressed") == "false"

    page.reload()

    assert page.locator("html").get_attribute("data-theme") == "light"
    assert page.locator("#theme-toggle").inner_text() == "Dark Mode"


def test_home_page_has_no_js_exceptions(page, site_url):
    """Loading the page and toggling the theme raises no JS exceptions."""
    errors = _js_exceptions(page)

    page.goto(site_url)
    page.locator("#theme-toggle").click()
    page.reload()

    assert errors == []


def test_favicon_is_the_computer_icon(page, site_url):
    """The tab icon points at the shared computer core asset."""
    page.goto(site_url)

    assert page.locator("link[rel='icon']").get_attribute("href") == (
        "assets/core-assets/icons/computer.svg"
    )
