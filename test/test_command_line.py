# coding=utf-8
"""
Tests
"""
import os
import sys
import subprocess
initial_pwd= os.getcwd()
here = os.path.abspath(os.path.dirname(__file__))
PROJECT = "find_known_secrets"
SRC = here + "/.."

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

def execute_get_text(command):
    try:
        result = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True)
        print(result.decode())
    except subprocess.CalledProcessError as err:
        print(err)
        # try:
        #     print(err.stdout)
        # except:
        #     pass
        # try:
        #     print(err.stderr)
        # except:
        #     pass
        raise

    return result.decode('utf-8')

def test_default():
    try:
        os.chdir(SRC)
        result = execute_get_text("python -m find_known_secrets here")
        print(result)
    finally:
        os.chdir("test")


def test_self_version():
    try:
        os.chdir(SRC)
        print(os.getcwd())
        result = execute_get_text("python -m find_known_secrets --version")
        print(result)
        assert "." in result.split("Find Known Secrets")[1]
    finally:
        os.chdir(initial_pwd)

def test_self_help():
    try:
        os.chdir(SRC)
        print(os.getcwd())
        result = execute_get_text("python -m find_known_secrets --help")
        print(result)
        assert result
    finally:
        os.chdir(initial_pwd)
