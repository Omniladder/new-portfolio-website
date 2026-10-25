import jinja2

from src.errors.generate_pages import PageGenerationError
from src.utils.log import get_logger, pluralize
from src.utils.render import render_template_to_dist

_log = get_logger("generate_pages")


def generate_pages(data: dict) -> None:
    """Generate every static HTML page for the site.

    Args:
        data: Parsed, schema-validated site content (see parse_data()).

    Returns:
        None.
    """
    generate_home(data)
    generate_projects_home(data)
    generate_projects(data)
    generate_education(data)
    generate_experience(data)

    project_count = len(data.get("projects", []))
    _log.info(
        "Rendered %s (home, projects index, %s, education, experience)",
        pluralize(project_count + 4, "page"),
        pluralize(project_count, "project page"),
    )


def generate_home(data: dict) -> None:
    """Generate the home page at dist/index.html.

    Args:
        data: Parsed, schema-validated site content (see parse_data()).

    Returns:
        None.

    Raises:
        PageGenerationError: If home.html can't be rendered or written.
    """
    try:
        render_template_to_dist("home.html", data, output_path="index.html")
    except (jinja2.TemplateError, OSError) as e:
        raise PageGenerationError(f"Failed to generate the home page: {e}") from e


def generate_projects_home(data: dict) -> None:
    """Generate the projects index page at dist/projects/index.html.

    Args:
        data: Parsed, schema-validated site content (see parse_data()).

    Returns:
        None.

    Raises:
        PageGenerationError: If project_home.html can't be rendered or written.
    """
    try:
        render_template_to_dist(
            "project_home.html", data, output_path="projects/index.html"
        )
    except (jinja2.TemplateError, OSError) as e:
        raise PageGenerationError(
            f"Failed to generate the projects index page: {e}"
        ) from e


def generate_projects(data: dict) -> None:
    """Generate a page for every project listed in data["projects"].

    Each entry is rendered through templates/project.html to
    dist/projects/<project_name>/index.html, so each project gets a clean
    URL. See docs/arch/0010 for why this is data-driven rather than one
    template file per project.

    Args:
        data: Parsed, schema-validated site content (see parse_data()).

    Returns:
        None.

    Raises:
        PageGenerationError: If a project's page can't be rendered or
            written. The message names the failing project's slug.
    """
    for project in data.get("projects", []):
        slug = project["project_name"]
        try:
            render_template_to_dist(
                "project.html",
                {**data, "project": project},
                output_path=f"projects/{slug}/index.html",
            )
        except (jinja2.TemplateError, OSError) as e:
            raise PageGenerationError(
                f"Failed to generate the project page for '{slug}': {e}"
            ) from e


def generate_education(data: dict) -> None:
    """Generate the education page at dist/education/index.html.

    Args:
        data: Parsed, schema-validated site content (see parse_data()).

    Returns:
        None.

    Raises:
        PageGenerationError: If education.html can't be rendered or written.
    """
    try:
        render_template_to_dist(
            "education.html", data, output_path="education/index.html"
        )
    except (jinja2.TemplateError, OSError) as e:
        raise PageGenerationError(f"Failed to generate the education page: {e}") from e


def generate_experience(data: dict) -> None:
    """Generate the experience page at dist/experience/index.html.

    Args:
        data: Parsed, schema-validated site content (see parse_data()).

    Returns:
        None.

    Raises:
        PageGenerationError: If experience.html can't be rendered or written.
    """
    try:
        render_template_to_dist(
            "experience.html", data, output_path="experience/index.html"
        )
    except (jinja2.TemplateError, OSError) as e:
        raise PageGenerationError(f"Failed to generate the experience page: {e}") from e
