""" nox session definition """

import os
from typing import Any
import subprocess

import nox

locations = "src", "noxfile.py"


# https://cjolowicz.github.io/posts/hypermodern-python-02-testing/
# https://cjolowicz.github.io/posts/hypermodern-python-03-linting/


@nox.session(python=None)
def black(session: Any) -> None:
    """runs black to do some automatic code automatisation"""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python=None)
def lint(session: Any) -> None:
    """runs the linter to inspect the code"""
    args = session.posargs or locations
    session.install(
        "flake8",
        # "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
    )
    session.run("flake8", *args)


@nox.session(python=None)
def tests(session: Any) -> None:
    """runs a test session"""
    session.run(
        "docker",
        "run",
        "--rm",
        "-v",
        f"{os.getcwd()}:/app",
        "operational_wind_solar:latest",
        "pytest",
        "tests/",
    )


@nox.session(python=None)
def push_image_to_ecr(session: Any) -> None:
    """This session updates the ecr docker image that will be used for operational use."""
    ecr_password = subprocess.run(
        ["aws", "ecr", "get-login-password", "--region", "eu-central-1"],
        capture_output=True,
        text=True,
    ).stdout.replace("\n", "")
    session.run(
        "docker",
        "login",
        "-u",
        "AWS",
        "-p",
        ecr_password,
        "661115856326.dkr.ecr.eu-central-1.amazonaws.com",
    )
    session.run(
        "docker",
        "tag",
        "operational_wind_solar",
        "661115856326.dkr.ecr.eu-central-1.amazonaws.com/operational_wind_solar",
    )
    session.run(
        "docker",
        "push",
        "661115856326.dkr.ecr.eu-central-1.amazonaws.com/operational_wind_solar",
    )
