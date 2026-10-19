import pytest

from src.errors.generate_pages import PageGenerationError
from src.operations import generate_pages as generate_pages_module
from src.operations.generate_pages import (
    generate_home,
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


def test_generate_pages_calls_generate_home_and_generate_projects(monkeypatch):
    """generate_pages generates the home page, projects index, and project pages."""
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
    data = {"name": "someone"}

    generate_pages(data)

    assert calls == [("home", data), ("projects_home", data), ("projects", data)]
