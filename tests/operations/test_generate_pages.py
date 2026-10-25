import logging

import pytest

from src.errors.generate_pages import PageGenerationError
from src.operations import generate_pages as generate_pages_module
from src.operations.generate_pages import (
    generate_education,
    generate_experience,
    generate_home,
    generate_not_found,
    generate_pages,
    generate_projects,
    generate_projects_home,
)


def _broken_render(*args, **kwargs):
    raise OSError("disk error")


def test_generate_home_renders_home_template(monkeypatch):
    """generate_home renders templates/home.html to dist/index.html."""
    calls = []
    monkeypatch.setattr(
        generate_pages_module,
        "render_template_to_dist",
        lambda template_path, data, output_path=None: calls.append(
            (template_path, data, output_path)
        ),
    )
    data = {"name": "someone"}

    generate_home(data)

    assert calls == [("home.html", data, "index.html")]


def test_generate_home_raises_on_render_failure(monkeypatch):
    """A render failure raises PageGenerationError naming the home page."""
    monkeypatch.setattr(
        generate_pages_module, "render_template_to_dist", _broken_render
    )

    with pytest.raises(PageGenerationError, match="home page"):
        generate_home({"name": "someone"})


def test_generate_projects_home_renders_project_home_template(monkeypatch):
    """generate_projects_home renders project_home.html to dist/projects/index.html."""
    calls = []
    monkeypatch.setattr(
        generate_pages_module,
        "render_template_to_dist",
        lambda template_path, data, output_path=None: calls.append(
            (template_path, data, output_path)
        ),
    )
    data = {"name": "someone"}

    generate_projects_home(data)

    assert calls == [("project_home.html", data, "projects/index.html")]


def test_generate_projects_home_raises_on_render_failure(monkeypatch):
    """A render failure raises PageGenerationError naming the projects index page."""
    monkeypatch.setattr(
        generate_pages_module, "render_template_to_dist", _broken_render
    )

    with pytest.raises(PageGenerationError, match="projects index page"):
        generate_projects_home({"name": "someone"})


def test_generate_projects_renders_every_entry_in_data(monkeypatch):
    """generate_projects renders project.html once per entry in data["projects"]."""
    calls = []
    monkeypatch.setattr(
        generate_pages_module,
        "render_template_to_dist",
        lambda template_path, data, output_path=None: calls.append(
            (template_path, data, output_path)
        ),
    )
    data = {
        "name": "someone",
        "projects": [
            {"project_name": "example_project"},
            {"project_name": "another_project"},
        ],
    }

    generate_projects(data)

    assert calls == [
        (
            "project.html",
            {**data, "project": data["projects"][0]},
            "projects/example_project/index.html",
        ),
        (
            "project.html",
            {**data, "project": data["projects"][1]},
            "projects/another_project/index.html",
        ),
    ]


def test_generate_projects_raises_on_render_failure(monkeypatch):
    """A render failure raises PageGenerationError naming the failing project."""
    monkeypatch.setattr(
        generate_pages_module, "render_template_to_dist", _broken_render
    )
    data = {"projects": [{"project_name": "example_project"}]}

    with pytest.raises(PageGenerationError, match="example_project"):
        generate_projects(data)


def test_generate_education_renders_education_template(monkeypatch):
    """generate_education renders education.html to dist/education/index.html."""
    calls = []
    monkeypatch.setattr(
        generate_pages_module,
        "render_template_to_dist",
        lambda template_path, data, output_path=None: calls.append(
            (template_path, data, output_path)
        ),
    )
    data = {"name": "someone"}

    generate_education(data)

    assert calls == [("education.html", data, "education/index.html")]


def test_generate_education_raises_on_render_failure(monkeypatch):
    """A render failure raises PageGenerationError naming the education page."""
    monkeypatch.setattr(
        generate_pages_module, "render_template_to_dist", _broken_render
    )

    with pytest.raises(PageGenerationError, match="education page"):
        generate_education({"name": "someone"})


def test_generate_experience_renders_experience_template(monkeypatch):
    """generate_experience renders experience.html to dist/experience/index.html."""
    calls = []
    monkeypatch.setattr(
        generate_pages_module,
        "render_template_to_dist",
        lambda template_path, data, output_path=None: calls.append(
            (template_path, data, output_path)
        ),
    )
    data = {"name": "someone"}

    generate_experience(data)

    assert calls == [("experience.html", data, "experience/index.html")]


def test_generate_experience_raises_on_render_failure(monkeypatch):
    """A render failure raises PageGenerationError naming the experience page."""
    monkeypatch.setattr(
        generate_pages_module, "render_template_to_dist", _broken_render
    )

    with pytest.raises(PageGenerationError, match="experience page"):
        generate_experience({"name": "someone"})


def test_generate_not_found_renders_404_template(monkeypatch):
    """generate_not_found renders templates/404.html to dist/404.html."""
    calls = []
    monkeypatch.setattr(
        generate_pages_module,
        "render_template_to_dist",
        lambda template_path, data, output_path=None: calls.append(
            (template_path, data, output_path)
        ),
    )
    data = {"name": "someone"}

    generate_not_found(data)

    assert calls == [("404.html", data, "404.html")]


def test_generate_not_found_raises_on_render_failure(monkeypatch):
    """A render failure raises PageGenerationError naming the 404 page."""
    monkeypatch.setattr(
        generate_pages_module, "render_template_to_dist", _broken_render
    )

    with pytest.raises(PageGenerationError, match="404 page"):
        generate_not_found({"name": "someone"})


def test_generate_pages_calls_every_page_generator(monkeypatch):
    """generate_pages generates every page, including the 404 page."""
    calls = []
    monkeypatch.setattr(
        generate_pages_module,
        "generate_home",
        lambda data: calls.append(("home", data)),
    )
    monkeypatch.setattr(
        generate_pages_module,
        "generate_projects_home",
        lambda data: calls.append(("projects_home", data)),
    )
    monkeypatch.setattr(
        generate_pages_module,
        "generate_projects",
        lambda data: calls.append(("projects", data)),
    )
    monkeypatch.setattr(
        generate_pages_module,
        "generate_education",
        lambda data: calls.append(("education", data)),
    )
    monkeypatch.setattr(
        generate_pages_module,
        "generate_experience",
        lambda data: calls.append(("experience", data)),
    )
    monkeypatch.setattr(
        generate_pages_module,
        "generate_not_found",
        lambda data: calls.append(("not_found", data)),
    )
    data = {"name": "someone"}

    generate_pages(data)

    assert calls == [
        ("home", data),
        ("projects_home", data),
        ("projects", data),
        ("education", data),
        ("experience", data),
        ("not_found", data),
    ]


def test_generate_pages_logs_page_count(monkeypatch, caplog):
    """generate_pages logs the total pages rendered, broken down by kind."""
    caplog.set_level(logging.INFO, logger="portfolio")
    for name in (
        "generate_home",
        "generate_projects_home",
        "generate_projects",
        "generate_education",
        "generate_experience",
        "generate_not_found",
    ):
        monkeypatch.setattr(generate_pages_module, name, lambda data: None)
    data = {"projects": [{"project_name": "example_project"}]}

    generate_pages(data)

    assert (
        "Rendered 6 pages (home, projects index, 1 project page, education, "
        "experience, 404)" in caplog.text
    )
