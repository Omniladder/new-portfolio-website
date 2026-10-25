"""End-to-end checks for the education page's content (docs/arch/0036).

Driven by whatever data.json's optional `education` list holds; without one,
only the placeholder is checked. See docs/arch/0019, 0033.
"""

import pytest


@pytest.fixture
def education_page(page, site_url):
    page.goto(f"{site_url}/education/index.html")
    return page


def _schools(site_data):
    return site_data.get("education") or []


def test_placeholder_only_without_education(education_page, site_data):
    """With no education entries, the page shows the placeholder instead."""
    placeholder = education_page.locator(".education-intro")
    if _schools(site_data):
        assert placeholder.count() == 0
    else:
        assert placeholder.count() == 1


def test_each_school_has_a_hero(education_page, site_data):
    """Every school renders its name and degree in a hero, in data.json order."""
    schools = _schools(site_data)
    titles = education_page.locator(".education-hero .project-title")

    assert titles.all_inner_texts() == [s["school"] for s in schools]
    for i, school in enumerate(schools):
        kicker = education_page.locator(".education-kicker").nth(i).inner_text()
        assert school["degree"].lower() in kicker.lower()


def test_transcript_lists_every_course(education_page, site_data):
    """Every course in every term appears once in the transcript."""
    expected = [
        c["code"]
        for school in _schools(site_data)
        for term in school.get("terms", [])
        for c in term["courses"]
    ]
    codes = education_page.locator("details.course .course-code")

    assert codes.all_inner_texts() == expected


def test_course_details_open_on_click(education_page, site_data):
    """Clicking a course's summary reveals its description."""
    courses = [
        c
        for school in _schools(site_data)
        for term in school.get("terms", [])
        for c in term["courses"]
    ]
    if not courses:
        pytest.skip("data.json has no courses")
    first = education_page.locator("details.course").first

    assert first.get_attribute("open") is None
    first.locator("summary").click()

    assert first.get_attribute("open") is not None
    if courses[0].get("description"):
        assert first.locator(".course-body").is_visible()


def test_gpa_chart_has_a_bar_per_graded_term(education_page, site_data):
    """The GPA chart has one row per term that sets a gpa, oldest first."""
    for i, school in enumerate(_schools(site_data)):
        graded = [t for t in school.get("terms", []) if "gpa" in t]
        rows = education_page.locator(f"#school-{i + 1}-gpa .gpa-term")
        assert rows.all_inner_texts() == [t["name"] for t in reversed(graded)]


def test_course_project_links_resolve(education_page, site_data, site_url):
    """Every course project link points at an existing project page."""
    slugs = {p["project_name"] for p in site_data["projects"]}
    links = education_page.locator(".course-project-list a")

    for href in links.evaluate_all("els => els.map(e => e.getAttribute('href'))"):
        slug = href.removeprefix("../projects/").removesuffix("/index.html")
        assert slug in slugs
        response = education_page.request.get(f"{site_url}/projects/{slug}/index.html")
        assert response.ok
