"""Regression checks for the public alpha's documented release contract."""

import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[2]


def test_project_status_matches_published_alpha() -> None:
    status = (ROOT / "docs" / "PROJECT_STATUS.md").read_text(encoding="utf-8")
    assert "Published release commit: `1082917`" in status
    assert "Published tag: `v0.1.0-alpha`" in status
    assert "not been published to\nPyPI" in status
    assert "not been tagged" not in status


def test_public_release_documents_required_boundaries() -> None:
    required = (
        "LICENSE",
        "NOTICE",
        "THIRD_PARTY_NOTICES.md",
        "README.md",
        "KNOWN_LIMITATIONS.md",
        "VALIDATION_REPORT.md",
        "SUPPORTED_FEATURES.md",
        "RELEASE_NOTES_v0.1.0-alpha.md",
    )
    for filename in required:
        assert (ROOT / filename).is_file(), filename

    supported = (ROOT / "SUPPORTED_FEATURES.md").read_text(encoding="utf-8")
    assert "Experimental opt-in profile" in supported
    assert "disabled by default" in supported


def test_release_tag_and_build_outputs_are_not_tracked() -> None:
    tracked = set(
        subprocess.check_output(("git", "ls-files"), cwd=ROOT, text=True).splitlines()
    )
    forbidden_fragments = (".release-venv/", ".venv312/", "dist/", "build/")
    assert not any(any(fragment in item for fragment in forbidden_fragments) for item in tracked)
