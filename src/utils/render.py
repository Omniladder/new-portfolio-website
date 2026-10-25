from datetime import date

import jinja2

from src.utils.paths import DIST_DIR, ROOT_DIR, TEMPLATES_DIR


def inline_svg(relative_path: str) -> str:
    """Read an SVG file's contents for inline embedding in a template.

    Embedding the markup directly, instead of referencing the file from an
    <img> or a CSS mask-image, means the icon always renders even when the
    page is opened via file:// rather than a server (an unreliable load for
    external mask/image resources in some browsers), and keeps it
    theme-aware, since a `fill="currentColor"` in the source SVG resolves
    against the surrounding page's CSS once it's truly inline. See
    docs/arch/0021. Use with Jinja's `| safe` filter at the call site.

    Args:
        relative_path: Path to the SVG file, relative to ROOT_DIR.

    Returns:
        str: The file's raw contents.
    """
    return (ROOT_DIR / relative_path).read_text()


def build_month() -> str:
    """Return the current month, for templates that need to know "now".

    The experience page uses it as the end of a current job ("Present") on
    its timeline and in job durations. See docs/arch/0037.

    Returns:
        str: Today's year and month as ``YYYY-MM``.
    """
    return date.today().strftime("%Y-%m")


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
    environment.globals["inline_svg"] = inline_svg
    environment.globals["build_month"] = build_month()
    template = environment.get_template(template_path)
    rendered = template.render(**data)

    destination = DIST_DIR / output_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(rendered)
