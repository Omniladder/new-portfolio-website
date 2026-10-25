"""End-to-end checks for the experience page's content (docs/arch/0037).

Driven by whatever data.json's optional `experience` section holds; without
one, only the placeholder is checked. See docs/arch/0019, 0033.
"""

import pytest


@pytest.fixture
def experience_page(page, site_url):
    page.goto(f"{site_url}/experience/index.html")
    return page


def _experience(site_data):
    return site_data.get("experience") or {}


def _has_content(xp):
    return any(xp.get(key) for key in ("positions", "events", "certifications"))


def test_placeholder_only_without_experience(experience_page, site_data):
    """With no positions, events, or certifications, the page shows the placeholder."""
    placeholder = experience_page.locator(".experience-intro")
    if _has_content(_experience(site_data)):
        assert placeholder.count() == 0
    else:
        assert placeholder.count() == 1


def test_hero_shows_current_role(experience_page, site_data):
    """A first position with no end date is shown in the hero as the current role."""
    positions = _experience(site_data).get("positions", [])
    if not positions or "end" in positions[0]:
        pytest.skip("data.json has no current position")
    hero = experience_page.locator(".experience-hero")

    assert hero.locator(".project-title").inner_text() == positions[0]["title"]
    assert "Present" in hero.inner_text()


def test_work_history_lists_every_position(experience_page, site_data):
    """Every position appears once in Work History, in data.json order."""
    positions = _experience(site_data).get("positions", [])
    titles = experience_page.locator(".job .job-title")

    assert titles.all_inner_texts() == [p["title"] for p in positions]


def test_timeline_has_a_bar_per_position(experience_page, site_data):
    """The timeline has one bar per position, and ongoing ones are marked."""
    positions = _experience(site_data).get("positions", [])
    bars = experience_page.locator(".xp-bar")

    assert bars.count() == len(positions)
    ongoing = [p for p in positions if "end" not in p]
    assert experience_page.locator(".xp-bar.is-current").count() == len(ongoing)


def test_timeline_marks_every_event_and_award(experience_page, site_data):
    """Each event gets a marker, starred when it won an award."""
    events = _experience(site_data).get("events", [])
    markers = experience_page.locator(".xp-marker:not(.is-cert)")

    assert markers.count() == len(events)
    winners = [e for e in events if e.get("awards")]
    assert experience_page.locator(".xp-marker.has-award").count() == len(winners)


def test_event_cards_list_every_event(experience_page, site_data):
    """Every event appears once as a card, with each of its awards."""
    events = _experience(site_data).get("events", [])
    names = experience_page.locator(".event-card .event-name")

    assert names.all_inner_texts() == [e["name"] for e in events]
    awards = experience_page.locator(".event-card .award")
    assert awards.count() == sum(len(e.get("awards", [])) for e in events)


def test_event_images_shown_without_project(experience_page, site_data, site_url):
    """Events with an image and no project show that image, and it loads (0038)."""
    events = _experience(site_data).get("events", [])
    slugs = {p["project_name"] for p in site_data["projects"]}
    imaged = [e for e in events if e.get("image") and e.get("project") not in slugs]
    images = experience_page.locator(".event-thumb-image img")

    assert images.count() == len(imaged)
    srcs = images.evaluate_all("els => els.map(e => e.getAttribute('src'))")
    for event, src in zip(imaged, srcs, strict=True):
        assert src.endswith(event["image"])
        assert experience_page.request.get(f"{site_url}/{event['image']}").ok


def test_project_links_resolve(experience_page, site_data, site_url):
    """Every job and event project link points at an existing project page."""
    slugs = {p["project_name"] for p in site_data["projects"]}
    links = experience_page.locator(
        ".job-projects a, .event-card a[href^='../projects/']"
    )

    for href in links.evaluate_all("els => els.map(e => e.getAttribute('href'))"):
        slug = href.removeprefix("../projects/").removesuffix("/index.html")
        assert slug in slugs
        response = experience_page.request.get(f"{site_url}/projects/{slug}/index.html")
        assert response.ok


def test_toolbox_lists_each_technology_once(experience_page, site_data):
    """The Toolbox shows every technology from every position exactly once."""
    names = {
        t["name"]
        for p in _experience(site_data).get("positions", [])
        for t in p.get("technologies", [])
    }
    tools = experience_page.locator(
        ".toolbox-grid li > span:not(.toolbox-count):not(.toolbox-glyph)"
    )

    shown = tools.all_inner_texts()
    assert sorted(shown) == sorted(names)
