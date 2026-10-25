"""Shared fixtures for the Playwright end-to-end suite.

These tests drive a real browser against the generated site, so they're kept
out of the default pytest run (see tests/conftest.py's collect_ignore) and
run explicitly with ``pytest tests/playwright``, after a one-time
``playwright install chromium``. The site is built from the real data.json
only; if it's missing, the whole suite is skipped. See docs/arch/0019, 0033.
"""

import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT_DIR / "data.json"


def _free_port() -> int:
    """Find an unused TCP port on localhost.

    Returns:
        int: A port number currently free to bind to.
    """
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _wait_until_serving(url: str, timeout: float = 10.0) -> None:
    """Block until a GET request to url succeeds, or raise after timeout.

    Args:
        url: URL to poll.
        timeout: Seconds to wait before giving up.

    Returns:
        None.

    Raises:
        RuntimeError: If the server doesn't respond within timeout.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1).close()
            return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"Server at {url} did not start within {timeout}s")


@pytest.fixture(scope="session")
def site_data():
    """Load the real data.json the site is built from, read-only.

    Tests derive what they expect from this instead of hardcoding content,
    so they pass for any fork's data.json. There is no data.template.json
    fallback (docs/arch/0033): if data.json is missing, every test that
    depends on this fixture is skipped.

    Returns:
        dict: The parsed contents of data.json.
    """
    if not DATA_PATH.exists():
        pytest.skip("data.json not found; the e2e suite only runs against it")
    return json.loads(DATA_PATH.read_text())


@pytest.fixture(scope="session")
def site_url(site_data):
    """Build the site from data.json and serve it over HTTP.

    generate.py only reads data.json, so building from it is safe
    (docs/arch/0025). Images are copied as-is (--no-image-processing,
    docs/arch/0043): no test checks processed pixels, and it saves ~45 s.

    Args:
        site_data: Ensures data.json exists before building.

    Yields:
        str: Base URL of the running server, e.g. "http://127.0.0.1:51234".
    """
    subprocess.run(
        [sys.executable, "generate.py", "--no-image-processing"],
        cwd=ROOT_DIR,
        check=True,
        capture_output=True,
    )

    port = _free_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--directory", "dist"],
        cwd=ROOT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base_url = f"http://127.0.0.1:{port}"
    try:
        _wait_until_serving(base_url)
        yield base_url
    finally:
        server.terminate()
        server.wait(timeout=5)
