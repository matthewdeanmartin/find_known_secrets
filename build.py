# coding=utf-8
"""
Stop gap build script until I find something better.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
import sys
import functools
import glob
import json
import os
import socket
import subprocess

from checksumdir import dirhash
from pynt import task
from pyntcontrib import execute, safe_cd
from semantic_version import Version

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from build_utils import check_is_aws, skip_if_no_change, execute_with_environment, get_versions, get_packages


PROJECT_NAME = "find_known_secrets"
SRC = '.'

# generic python
PYTHON = "python"
IS_DJANGO = False
IS_TRAVIS = 'TRAVIS' in os.environ
if IS_TRAVIS:
    PIPENV = ""
else:
    PIPENV = "pipenv run"
GEM_FURY = ""

CURRENT_HASH = None

MAC_LIBS = ":..:"




@task()
@skip_if_no_change("git_secrets")
def git_secrets():
    if check_is_aws():
        # no easy way to install git secrets on ubuntu.
        return
    if IS_TRAVIS:
        # nothing is edited on travis
        return
    try:
        commands = ["git secrets --install", "git secrets --register-aws"]
        for command in commands:
            cp = subprocess.run(command.split(" "),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                shell=False, check=True)
            for stream in [cp.stdout, cp.stderr]:
                if stream:
                    for line in stream.decode().split("\n"):
                        print("*" + line)
    except subprocess.CalledProcessError as cpe:
        print(cpe)
        installed = False
        for stream in [cpe.stdout, cpe.stderr]:
            if stream:
                for line in stream.decode().split("\n"):
                    print("-" + line)
                    if "commit-msg already exists" in line:
                        print("git secrets installed.")
                        installed = True
                        break
        if not installed:
            raise
    execute(*("git secrets --scan".strip().split(" ")))


@task()
def clean():
    return


@task()
@skip_if_no_change("formatting")
def formatting():
    with safe_cd(SRC):
        if sys.version_info < (3, 6):
            print("Black doesn't work on python 2")
            return
        command = "{0} black {1}".format(PIPENV, PROJECT_NAME).strip()
        print(command)
        execute(*(command.split(" ")))


@task(clean)
@skip_if_no_change("compile")
def compile():
    with safe_cd(SRC):
        execute(PYTHON, "-m", "compileall", PROJECT_NAME)


@task(compile)
@skip_if_no_change("prospector")
def prospector():
    with safe_cd(SRC):
        command = "{0} prospector {1} --profile {1}_style --pylint-config-file=pylintrc.ini --profile-path=.prospector" \
            .format(PIPENV, PROJECT_NAME).strip().replace("  ", " ")
        print(command)
        execute(*(command
                  .split(" ")))


@task()
@skip_if_no_change("detect_secrets")
def detect_secrets():
    # use
    # blah blah = "foo"     # pragma: whitelist secret
    # to ignore a false posites
    errors_file = "detect-secrets-results.json"

    command = "detect-secrets --scan --base64-limit 4 --exclude .idea|.js|.min.js|.html|.xsd|" \
              "lock.json|synced_folders|.scss|" \
              "lint.txt|{0}".format(errors_file)
    print(command)
    bash_process = subprocess.Popen(command.split(" "),
                                    # shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE
                                    )
    out, err = bash_process.communicate()  # wait

    with open(errors_file, "w+") as file_handle:
        file_handle.write(out.decode())


    with open(errors_file) as f:
        try:
            data = json.load(f)
            if data["results"]:
                for result in data["results"]:
                    print(result)
                print("detect-secrets has discovered high entropy strings, possibly passwords?")
                exit(-1)
                return
                # raise TypeError("detect-secrets has discovered high entropy strings, possibly passwords?")
        except Exception:
            print("Can't read json")


@task(compile, formatting, prospector)
@skip_if_no_change("lint")
def lint():
    with safe_cd(SRC):
        if os.path.isfile("lint.txt"):
            execute("rm", "lint.txt")

    with safe_cd(SRC):
        if IS_DJANGO:
            django_bits = "--load-plugins pylint_django "
        else:
            django_bits = ""

        # command += "{0}--rcfile=pylintrc.ini {1}".format(django_bits, PROJECT_NAME).split(" ")
        command = "{0} pylint {1} --rcfile=pylintrc.ini {2}".format(PIPENV, django_bits, PROJECT_NAME) \
            .strip() \
            .replace("  ", " ")
        print(command)
        command = command.split(" ")

        # keep out of src tree, causes extraneous change detections
        lint_output_file_name = "lint.txt"
        with open(lint_output_file_name, "w") as outfile:
            env = config_pythonpath()
            subprocess.call(command, stdout=outfile, env=env)

        fatal_errors = sum(1 for line in open(lint_output_file_name)
                           if "no-member" in line or \
                           "no-name-in-module" in line or \
                           "import-error" in line)

        if fatal_errors > 0:
            for line in open(lint_output_file_name):
                if "no-member" in line or \
                        "no-name-in-module" in line or \
                        "import-error" in line:
                    print(line)
            print("Fatal lint errors : {0}".format(fatal_errors))
            exit(-1)
            return

        cutoff = 69
        num_lines = sum(1 for line in open(lint_output_file_name)
                        if "*************" not in line
                        and "---------------------" not in line
                        and "Your code has been rated at" not in line)
        if num_lines > cutoff:
            print("Too many lines of lint : {0}".format(num_lines))
            exit(-1)
            return


@task()
@skip_if_no_change("nose_tests")
def nose_tests():
    if IS_DJANGO:
        command = "{0} manage.py test -v 2".format(PYTHON)
        # We'd expect this to be MAC or a build server.
        my_env = config_pythonpath()
        execute_with_environment(command, env=my_env)
    else:
        my_env = config_pythonpath()
        command = "{0} {1} -m nose {2}".format(PIPENV, PYTHON, "test").strip()
        print(command)
        execute_with_environment(command, env=my_env)


def config_pythonpath():
    if check_is_aws():
        env = "DEV"
    else:
        env = "MAC"
    my_env = {'ENV': env}
    for key, value in os.environ.items():
        my_env[key] = value
    my_env["PYTHONPATH"] = my_env.get("PYTHONPATH",
                                      "") + MAC_LIBS
    print(my_env["PYTHONPATH"])
    return my_env


@task()
def coverage():
    print("Coverage tests always re-run")
    with safe_cd(SRC):
        my_env = config_pythonpath()
        command = "{0} py.test {1} --cov={2} --cov-report html:coverage --cov-fail-under 60  --verbose".format(
            PIPENV,
            "test", PROJECT_NAME)
        print(command)
        execute_with_environment(command, my_env)


@task()
@skip_if_no_change("docs")
def docs():
    with safe_cd(SRC):
        with safe_cd("docs"):
            my_env = config_pythonpath()
            execute_with_environment("pipenv run make html", env=my_env)


@task()
def pip_check():
    print("pip_check always reruns")
    with safe_cd(SRC):
        execute("pipenv", "check")


@task()
def compile_mark_down():
    with safe_cd(SRC):
        if IS_TRAVIS:
            command = "pandoc --from=markdown --to=rst --output=README.rst README.md".strip().split(
                " ")
        else:
            command = "{0} pandoc --from=markdown --to=rst --output=README.rst README.md".format(PIPENV).strip().split(
                " ")
        execute(*(command))


@task()
@skip_if_no_change("mypy")
def mypy():
    if sys.version_info < (3, 4):
        print("Mypy doesn't work on python < 3.4")
        return
    mypy_file = "mypy_errors.txt"
    if os.path.isfile(mypy_file):
        execute("rm", mypy_file)
    command = "{0} mypy {1} --ignore-missing-imports --strict".format(PIPENV, PROJECT_NAME).strip()
    bash_process = subprocess.Popen(command.split(" "),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE
                                    )
    out, err = bash_process.communicate()  # wait

    with open(mypy_file, "w+") as lint_file:
        lines = out.decode().split("\n")
        for line in lines:
            if "test.py" in line:
                continue
            if "tests.py" in line:
                continue
            if "/test_" in line:
                continue
            if "/tests_" in line:
                continue
            else:
                lint_file.writelines([line + "\n"])

    num_lines = sum(1 for line in open(mypy_file) if line.strip())
    max_lines = 2
    if num_lines > max_lines:
        print("Too many lines of mypy : {0}, max {1}".format(num_lines, max_lines))
        exit(-1)
        return

@task()
def pin_dependencies():
    with safe_cd(SRC):
        execute(*("{0} pipenv_to_requirements".format(PIPENV).strip().split(" ")))



@task()
@skip_if_no_change("vulture", expect_files="dead_code.txt")
def dead_code():
    """
    This also finds code you are working on today!
    """
    with safe_cd(SRC):
        if IS_TRAVIS:
            command = "{0} vulture {1}".format(PYTHON, PROJECT_NAME).strip().split()
        else:
            command = "{0} vulture {1}".format(PIPENV, PROJECT_NAME).strip().split()

        output_file_name = "dead_code.txt"
        with open(output_file_name, "w") as outfile:
            env = config_pythonpath()
            subprocess.call(command, stdout=outfile, env=env)

        cutoff = 20
        num_lines = sum(1 for line in open(output_file_name) if line)
        if num_lines > cutoff:
            print("Too many lines of dead code : {0}, max {1}".format(num_lines, cutoff))
            exit(-1)

@task()
def jiggle_version():
    command = "{0} jiggle_version --project={1} --source={2}".format(PIPENV, PROJECT_NAME, "").strip()
    execute(*(command.split(" ")))


@task()
def check_setup_py():
    with safe_cd(SRC):
        if IS_TRAVIS:
            execute(PYTHON, *("setup.py check -r -s".split(" ")))
        else:
            execute(*("{0} {1} setup.py check -r -s".format(PIPENV, PYTHON).strip().split(" ")))

@task(formatting, mypy, detect_secrets, git_secrets, check_setup_py, nose_tests, coverage, compile, dead_code, lint,
      compile_mark_down, pin_dependencies, jiggle_version)
@skip_if_no_change("package")
def package():
    with safe_cd(SRC):
        for folder in ["build", "dist", PROJECT_NAME + ".egg-info"]:
            execute("rm", "-rf", folder)

    with safe_cd(SRC):
        execute(PYTHON, "setup.py", "sdist", "--formats=gztar,zip")


# FAST. FATAL ERRORS. DON'T CHANGE THINGS THAT CHECK IN
@task(mypy, detect_secrets, git_secrets, check_setup_py, compile, dead_code)
@skip_if_no_change("package")
def pre_commit_hook():
    # Don't format or update version
    # Don't do slow stuff- discourages frequent check in
    # Run checks that are likely to have FATAL errors, not just sloppy coding.
    pass

# Don't break the build, but don't change source tree either.
@task(mypy, detect_secrets, git_secrets, nose_tests, coverage, check_setup_py, compile, dead_code)
@skip_if_no_change("package")
def pre_push_hook():
    # Don't format or update version
    # Don't do slow stuff- discourages frequent check in
    # Run checks that are likely to have FATAL errors, not just sloppy coding.
    pass

@task(package)
def gemfury():
    """
    Upload to gemfury
    """
    # fury login
    #fury push dist/*.gz --as=YOUR_ACCT
    #fury push dist/*.whl --as=YOUR_ACCT

    cp = subprocess.run(("fury login --as={0}".format(GEM_FURY).split(" ")),
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        shell=False, check=True)
    print(cp.stdout)


    about = {}
    with open(os.path.join(SRC, PROJECT_NAME, "__version__.py")) as f:
        exec(f.read(), about)
    version = Version(about["__version__"])
    print("Have version : " + str(version))
    print("Preparing to upload")

    if version not in get_versions():
        for kind in ["gz", "whl"]:
            try:
                files = glob.glob("{0}dist/*.{1}".format(SRC.replace(".", ""), kind))
                for file_name in files:
                    cp = subprocess.run(("fury push {0} --as={1}".format(file_name, GEM_FURY).split(" ")),
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        shell=False, check=True)
                    print("result of fury push")
                    for stream in [cp.stdout, cp.stderr]:
                        if stream:
                            for line in stream.decode().split("\n"):
                                print(line)

            except subprocess.CalledProcessError as cpe:
                print("result of fury push- got error")
                for stream in [cp.stdout, cp.stderr]:
                    if stream:
                        for line in stream.decode().split("\n"):
                            print(line)
                print(cpe)
                raise


@task()
def echo(*args, **kwargs):
    print(args)
    print(kwargs)


# Default task (if specified) is run when no task is specified in the command line
# make sure you define the variable __DEFAULT__ after the task is defined
# A good convention is to define it at the end of the module
# __DEFAULT__ is an optional member

__DEFAULT__ = echo
