"""
Tests
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolate_credentials(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep default CLI scans away from the operator's credential files."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))


initial_pwd = os.getcwd()
here = os.path.abspath(os.path.dirname(__file__))
PROJECT = "find_known_secrets"
SRC = here + "/.."

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


def execute_get_text(arguments: list[str]) -> str:
    try:
        result = subprocess.check_output([sys.executable, "-m", PROJECT, *arguments], stderr=subprocess.STDOUT)
        print(result.decode())
    except subprocess.CalledProcessError as err:
        print(err)
        raise

    return result.decode("utf-8")


#
def test_found_custom_secrets():
    try:
        os.chdir(SRC)
        result = execute_get_text(["--secrets=test/secrets.ini"])
        print(result)
    except subprocess.CalledProcessError as cpe:
        assert "Failing this run" in str(cpe.stdout)
    finally:
        os.chdir(initial_pwd)


def test_default():
    try:
        os.chdir(SRC)
        result = execute_get_text(["here"])
        print(result)
    finally:
        os.chdir(initial_pwd)


def test_self_version():
    try:
        os.chdir(SRC)
        print(os.getcwd())
        result = execute_get_text(["--version"])
        print(result)
        assert "." in result.split("Find Known Secrets")[1]
    finally:
        os.chdir(initial_pwd)


def test_self_help():
    try:
        os.chdir(SRC)
        print(os.getcwd())
        result = execute_get_text(["--help"])
        print(result)
        assert result
    finally:
        os.chdir(initial_pwd)
