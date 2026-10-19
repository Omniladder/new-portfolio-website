import jinja2

from src.utils.paths import DIST_DIR, TEMPLATES_DIR


def render_template_to_dist(
    template_path: str, data: dict, output_path: str = None
) -> None:
    """Render a Jinja2 template with data and write it into dist/.

    Args:
        template_path: Path to the template, relative to TEMPLATES_DIR
            (e.g. ``"index.html"``).
        data: Render context passed to the template.
        output_path: Path, relative to DIST_DIR, to write the rendered
            output to, creating any missing parent directories. Defaults to
            template_path, for templates whose output location matches
            their own relative path.

    Returns:
        None.
    """
    if output_path is None:
        output_path = template_path

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_DIR))
    template = environment.get_template(template_path)
    rendered = template.render(**data)

    destination = DIST_DIR / output_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(rendered)
