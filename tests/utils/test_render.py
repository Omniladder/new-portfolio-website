from src.utils import render as render_module
from src.utils.render import render_template_to_dist


def _patch_dirs(monkeypatch, templates_dir, dist_dir):
    """Point render_template_to_dist's module-level path constants at fake dirs.

    Args:
        monkeypatch: pytest's monkeypatch fixture.
        templates_dir: fake templates directory to load templates from.
        dist_dir: fake dist directory to write rendered output into.
    """
    monkeypatch.setattr(render_module, "TEMPLATES_DIR", templates_dir)
    monkeypatch.setattr(render_module, "DIST_DIR", dist_dir)


def test_render_template_to_dist_renders_data_into_template(tmp_path, monkeypatch):
    """The template is rendered with the given data and written to dist/."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "index.html").write_text("<p>{{ name }}</p>")
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, templates_dir, dist_dir)

    render_template_to_dist("index.html", {"name": "someone"})

    assert (dist_dir / "index.html").read_text() == "<p>someone</p>"


def test_render_template_to_dist_creates_missing_directories(tmp_path, monkeypatch):
    """Nested output paths get their missing parent directories created."""
    templates_dir = tmp_path / "templates"
    (templates_dir / "nested").mkdir(parents=True)
    (templates_dir / "nested" / "page.html").write_text("ok")
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, templates_dir, dist_dir)

    render_template_to_dist("nested/page.html", {})

    assert (dist_dir / "nested" / "page.html").read_text() == "ok"


def test_render_template_to_dist_honors_output_path_override(tmp_path, monkeypatch):
    """An explicit output_path writes to a location other than template_path."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "project.html").write_text("<p>{{ name }}</p>")
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, templates_dir, dist_dir)

    render_template_to_dist(
        "project.html", {"name": "someone"}, output_path="projects/example/index.html"
    )

    assert not (dist_dir / "project.html").exists()
    assert (
        dist_dir / "projects" / "example" / "index.html"
    ).read_text() == "<p>someone</p>"
