"""Build the site once per test session and expose helpers to read it."""
import shutil
import subprocess
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
# `--environment test`: not production, so the CSS bundle is unminified and readable
# by the tests (CI's production build still minifies and fingerprints it).
HUGO = ["hugo", "--panicOnWarning", "--environment", "test", "--baseURL", "https://aquicirc.eu/"]
COPY_IGNORE = shutil.ignore_patterns(".git", ".pixi", ".superpowers", "public", "resources", "*.pdf", "*.txt")


def run_hugo(source: Path, destination: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [*HUGO, "--source", str(source), "--destination", str(destination)],
        capture_output=True, text=True,
    )


@pytest.fixture(scope="session")
def site(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("public")
    result = run_hugo(ROOT, out)
    assert result.returncode == 0, f"hugo failed:\n{result.stdout}\n{result.stderr}"
    return out


@pytest.fixture(scope="session")
def html(site):
    def load(path: str) -> BeautifulSoup:
        rel = path.strip("/")
        target = site / rel if rel.endswith((".html", ".xml")) else site / rel / "index.html"
        assert target.exists(), f"{path} was not built ({target})"
        return BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser")
    return load


@pytest.fixture(scope="session")
def css(site, html):
    def load() -> str:
        href = html("/").find("link", rel="stylesheet")["href"].split("?")[0]
        return (site / href.lstrip("/")).read_text(encoding="utf-8")
    return load


@pytest.fixture
def build_variant(tmp_path):
    """Copy the repo, let the test edit the copy, build it, return the result."""
    def build(edit) -> subprocess.CompletedProcess:
        src = tmp_path / "src"
        shutil.copytree(ROOT, src, ignore=COPY_IGNORE)
        edit(src)
        return run_hugo(src, tmp_path / "out")
    return build
