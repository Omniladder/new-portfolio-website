from src.utils import paths


def test_root_dir_points_to_repo_root():
    """ROOT_DIR should resolve to the directory containing generate.py."""
    assert (paths.ROOT_DIR / "generate.py").is_file()


def test_dist_dir_is_root_dir_slash_dist():
    """DIST_DIR is always ROOT_DIR/dist, never an absolute override."""
    assert paths.DIST_DIR == paths.ROOT_DIR / "dist"


def test_data_path_is_root_dir_slash_data_json():
    """DATA_PATH is always ROOT_DIR/data.json, never an absolute override."""
    assert paths.DATA_PATH == paths.ROOT_DIR / "data.json"


def test_data_template_path_is_root_dir_slash_data_template_json():
    """DATA_TEMPLATE_PATH is the tracked file forks copy to data.json."""
    assert paths.DATA_TEMPLATE_PATH == paths.ROOT_DIR / "data.template.json"


def test_data_schema_path_lives_under_src_schema():
    """The data schema is an internal build input under src/schema/, not a
    root-level directory a fork is meant to edit (see docs/arch/0008).
    """
    assert paths.SCHEMA_DIR == paths.ROOT_DIR / "src" / "schema"
    assert paths.DATA_SCHEMA_PATH == paths.SCHEMA_DIR / "data.schema.json"


def test_templates_dir_is_root_dir_slash_templates():
    """TEMPLATES_DIR is always ROOT_DIR/templates, never an absolute override."""
    assert paths.TEMPLATES_DIR == paths.ROOT_DIR / "templates"


def test_mirrored_dirs_excludes_build_inputs():
    """Directories consumed as build input must stay out of MIRRORED_DIRS.

    See docs/arch/0005 — templates/, docs/, src/, and data.json are inputs
    to generation, not assets carried through to dist/ verbatim.
    """
    assert "assets" in paths.MIRRORED_DIRS
    assert "static" in paths.MIRRORED_DIRS
    for excluded in ("templates", "docs", "src"):
        assert excluded not in paths.MIRRORED_DIRS
