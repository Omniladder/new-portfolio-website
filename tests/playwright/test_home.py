"""End-to-end checks for the rendered home page (templates/home.html).

Drives a real browser against the site built from data.template.json, so it
catches things unit tests can't: the theme toggle actually flips data-theme
and persists via localStorage, content from data.json actually renders, and
the page loads without console errors. See docs/arch/0019.
"""


def _js_exceptions(page):
    """Collect uncaught JS exceptions raised while page is used.

    Deliberately doesn't look at console "error" messages: data.template.json's
    placeholder asset paths (e.g. "assets/example.png") have no backing file,
    so the browser logs expected 404s that aren't a sign of anything broken in
    the page itself. This only tracks actual script exceptions.

    Args:
        page: Playwright Page to attach the listener to.

    Returns:
        list[str]: Exception message texts, appended to as they occur.
    """
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    return errors


def test_home_page_loads_in_light_theme_by_default(page, site_url):
    """With no stored preference, the page loads in light mode."""
    page.goto(site_url)

    assert page.title() == "Example Person — Software Engineer"
    assert page.locator("html").get_attribute("data-theme") == "light"
    assert page.locator(".site-name").inner_text() == "Example Person"


def test_top_nav_links_to_real_pages(page, site_url):
    """Home/Projects in the header nav are real page links, not anchors."""
    page.goto(site_url)
    top_nav = page.locator(".site-header .site-nav")

    assert top_nav.get_by_role("link", name="Home").get_attribute("href") == (
        "index.html"
    )
    assert top_nav.get_by_role("link", name="Projects").get_attribute("href") == (
        "projects/"
    )


def test_sidebar_quick_nav_and_sections_render(page, site_url):
    """The sidebar's in-page anchors and every section they point to exist."""
    page.goto(site_url)
    quick_nav = page.locator(".sidebar .nav-list")

    for label in [
        "About Me",
        "Skills",
        "Projects",
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


def test_featured_project_and_skills_render(page, site_url):
    """Content from data.template.json's projects/skills shows up on the page."""
    page.goto(site_url)

    assert (
        page.locator("#projects")
        .get_by_role("link", name="Example Project")
        .is_visible()
    )
    assert "Example Category" in page.locator(".skills-table").inner_text()
    assert "Example Technology" in page.locator(".skills-table").inner_text()


def test_theme_toggle_switches_and_persists_after_reload(page, site_url):
    """Clicking the toggle flips the theme and localStorage survives a reload."""
    page.goto(site_url)
    toggle = page.locator("#theme-toggle")

    assert page.locator("html").get_attribute("data-theme") == "light"
    assert toggle.inner_text() == "Dark Mode"

    toggle.click()

    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert toggle.inner_text() == "Light Mode"
    assert toggle.get_attribute("aria-pressed") == "true"

    page.reload()

    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert page.locator("#theme-toggle").inner_text() == "Light Mode"


def test_home_page_has_no_js_exceptions(page, site_url):
    """Loading the page and toggling the theme raises no JS exceptions."""
    errors = _js_exceptions(page)

    page.goto(site_url)
    page.locator("#theme-toggle").click()
    page.reload()

    assert errors == []
