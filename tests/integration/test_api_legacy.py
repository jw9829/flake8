"""Integration tests for the legacy api."""
from __future__ import annotations

import multiprocessing

from flake8.api import legacy


def test_legacy_api(tmpdir):
    """A basic end-to-end test for the legacy api reporting errors."""
    with tmpdir.as_cwd():
        t_py = tmpdir.join("t.py")
        t_py.write("import os  # unused import\n")

        style_guide = legacy.get_style_guide()
        report = style_guide.check_files([t_py.strpath])
        assert report.total_errors == 1


def test_legacy_api_options_are_used_by_spawned_workers(tmpdir, monkeypatch):
    monkeypatch.setattr(multiprocessing, "cpu_count", lambda: 2)
    monkeypatch.setattr(
        multiprocessing,
        "Pool",
        multiprocessing.get_context("spawn").Pool,
    )

    line = "x = " + repr("a" * 75) + "\n"
    paths = []
    for filename in ("one.py", "two.py"):
        path = tmpdir.join(filename)
        path.write(line)
        paths.append(path.strpath)

    style_guide = legacy.get_style_guide(max_line_length=88)
    report = style_guide.check_files(paths)
    assert report.total_errors == 0
