from __future__ import annotations

import os
import subprocess
from pathlib import Path

from fuzzy_couscous.utils import get_current_dir_as_project_name


def new_virtualenv(venv: str):
    if not Path(venv).expanduser().is_absolute():
        venv = str(Path(os.getcwd(), venv))
    else:
        venv = str(Path(venv, get_current_dir_as_project_name()))
    commands = [
        "python -m pip install --upgrade pip virtualenv",
        f"python -m virtualenv {venv}",
        f"{venv}/bin/python -m pip install pip-tools hatch",
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)


def compile_requirements(groups: list[str]):
    extras = " --extra " + " --extra ".join(groups) if groups else ""
    base_command = "venv/bin/python -m piptools compile -o requirements.txt pyproject.toml --resolver=backtracking"
    subprocess.run(
        [base_command + extras],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def install_dependencies():
    subprocess.run(
        ["venv/bin/python -m piptools sync"],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
