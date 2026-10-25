"""End-to-end checks for the 404 page.

The test server (python -m http.server) doesn't serve 404.html for missing
URLs the way nginx does, so the page is loaded directly. Its links are
root-absolute (docs/arch/0045), so they resolve the same from here as from
any missing URL. See docs/arch/0019, 0033.
"""

from tests.playwright.conftest import ROOT_DIR


def test_not_found_page_renders_with_header(page, site_url, site_data):
    """The 404 page shows the shared header and the error dialog."""
    page.goto(f"{site_url}/404.html")

    assert page.locator(".site-name").inner_text() == site_data["profile"]["name"]
    assert "404" in page.locator(".not-found-code").inner_text()
    assert page.locator(".error-dialog").is_visible()


def test_not_found_page_has_no_header_quote(page, site_url):
    """The 404 page isn't a section, so it shows no header quote."""
    page.goto(f"{site_url}/404.html")

    assert page.locator(".site-quote").count() == 0


def test_return_to_home_goes_to_home_page(page, site_url):
    """The Return to Home button navigates to the home page."""
    page.goto(f"{site_url}/404.html")

    page.get_by_role("link", name="Return to Home").click()

    assert page.url == f"{site_url}/index.html"
    assert page.locator(".site-header").is_visible()


def test_not_found_page_works_from_disk(page, site_url):
    """Opened via file://, the page is styled and Return to Home works."""
    not_found = ROOT_DIR / "dist" / "404.html"
    page.goto(not_found.as_uri())

    border = page.locator(".page").evaluate("el => getComputedStyle(el).borderTopStyle")
    assert border == "solid"
    page.get_by_role("link", name="Return to Home").click()
    assert page.url == (ROOT_DIR / "dist" / "index.html").as_uri()


def test_not_found_page_loads_styles(page, site_url):
    """The stylesheet loads via its root-absolute path, so the page is styled."""
    page.goto(f"{site_url}/404.html")

    border = page.locator(".page").evaluate("el => getComputedStyle(el).borderTopStyle")
    assert border == "solid"
