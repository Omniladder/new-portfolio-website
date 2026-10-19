"""Run the full test suite.

Lets the suite be run as ``python3 tests/test.py`` in addition to the plain
``pytest`` invocation. Named ``test.py`` (no trailing underscore) so pytest's
own discovery, which only collects ``test_*.py``, never picks this file up
as a test module itself.
"""

import sys
from pathlib import Path

import pytest


def main() -> int:
    """Discover and run every test_*.py module under tests/.

    Returns:
        int: pytest's process exit code (0 if all tests passed).
    """
    tests_dir = Path(__file__).resolve().parent
    return pytest.main([str(tests_dir)])


if __name__ == "__main__":
    sys.exit(main())
