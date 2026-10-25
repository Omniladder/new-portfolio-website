"""End-to-end checks for the education and experience pages.

These checks only confirm each page builds, is reachable from the header
nav, marks itself as current, and shows its quote only when data.json sets
one (docs/arch/0035). The education page's content is checked in
test_education.py (docs/arch/0036) and the experience page's in
test_experience.py (docs/arch/0037). See docs/arch/0019, 0033.
"""

import pytest

SECTIONS = ["education", "experience"]


@pytest.mark.parametrize("section", SECTIONS)
def test_section_page_renders_with_header(page, site_url, site_data, section):
    """The section page loads and its header nav marks it as the current page."""
    page.goto(f"{site_url}/{section}/index.html")

    assert page.locator(".site-name").inner_text() == site_data["profile"]["name"]
    current = page.locator(".site-header .site-nav [aria-current='page']")
    assert current.get_attribute("href") == f"../{section}/index.html"


@pytest.mark.parametrize("section", SECTIONS)
def test_section_quote_only_renders_when_set(page, site_url, site_data, section):
    """The header quote appears only if data.json sets quotes[section]."""
    page.goto(f"{site_url}/{section}/index.html")
    quote = site_data["quotes"].get(section)

    if quote:
        assert quote in page.locator(".site-quote").inner_text()
    else:
        assert page.locator(".site-quote").count() == 0


@pytest.mark.parametrize("section", SECTIONS)
def test_home_header_nav_links_to_section(page, site_url, section):
    """The home page's header nav links to each section page."""
    page.goto(site_url)
    top_nav = page.locator(".site-header .site-nav")

    link = top_nav.get_by_role("link", name=section.capitalize())
    assert link.get_attribute("href") == f"{section}/index.html"
