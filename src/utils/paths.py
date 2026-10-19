from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DIST_DIR = ROOT_DIR / "dist"
DATA_PATH = ROOT_DIR / "data.json"
DATA_TEMPLATE_PATH = ROOT_DIR / "data.template.json"
SCHEMA_DIR = ROOT_DIR / "src" / "schema"
DATA_SCHEMA_PATH = SCHEMA_DIR / "data.schema.json"
TEMPLATES_DIR = ROOT_DIR / "templates"

# Root-level directories whose path structure is mirrored into dist/, e.g.
# assets/download/ -> dist/assets/download/. See docs/arch/0005. Directories
# consumed as build input (templates/, docs/, src/, data.json) are deliberately
# excluded; their output path is decided by the operation that renders them.
MIRRORED_DIRS = ["assets", "static"]


def display_path(path: Path) -> str:
    """Format a path for log output, relative to ROOT_DIR when it's inside it.

    Args:
        path: The path to format. May be relative to the working directory.

    Returns:
        str: ``path`` relative to ROOT_DIR (e.g. ``"data.template.json"``),
        or its absolute form if it lies outside ROOT_DIR.
    """
    resolved = Path(path).resolve()
    try:
        return str(resolved.relative_to(ROOT_DIR))
    except ValueError:
        return str(resolved)
