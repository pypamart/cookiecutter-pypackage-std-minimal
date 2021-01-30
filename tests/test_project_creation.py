import logging
import os
import shutil
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter
from pytest_bdd import given, scenario, scenarios, then, when

logger = logging.getLogger()


@pytest.fixture(scope="module")
def dirpaths(tmp_path_factory):
    """
    Create an empty working directory
    """
    empty_working_directory = tmp_path_factory.getbasetemp()
    template_dirpath = Path.cwd()

    logger.info("Working directory :\n" + empty_working_directory.as_posix())

    try:
        yield {"template": template_dirpath, "cwd": empty_working_directory}
    finally:
        pass
        # shutil.rmtree(empty_working_directory)


@pytest.fixture()
def context_dict():
    return dict()


@scenario(
    "features/project_creation.feature",
    "Project creation",
    example_converters=dict(
        context_repository_name=str,
        context_package_name=str,
        real_repository_name=str,
        real_package_name=str,
        is_executable_package=str)

)
def test_project_creation():
    pass


@given("I am in a working project directory")
def go_to_working_dir(dirpaths):
    os.chdir(dirpaths["cwd"].as_posix())


@when("I configure the repository name as <context_repository_name> in the extra context")
def configure_context_repository_name(context_repository_name, context_dict):
    if context_repository_name:
        context_dict["repository_name"] = context_repository_name


@when("I configure the package name as <context_package_name> in the extra context")
def configure_context_package_name(context_package_name, context_dict):
    if context_package_name:
        context_dict["package_name"] = context_package_name


@when("I configure the package as executable = <is_executable_package>")
def configure_context_package_executability(is_executable_package, context_dict):
    context_dict["is_executable_package"] = is_executable_package


@when("I generate my project structure with this extra context")
def bake_with_extra_context(dirpaths, context_dict):
    cookiecutter(
        dirpaths["template"].as_posix(),
        extra_context=context_dict,
        no_input=True,
        overwrite_if_exists=True)


def check_if_directory(real_repository_name: pytest.fixture, subdirectory_name: str = ""):
    project_basepath = Path(".")
    path_name = real_repository_name + "/" + subdirectory_name

    assert project_basepath.joinpath(path_name).exists()
    assert project_basepath.joinpath(path_name).is_dir()


def check_if_file(real_repository_name: pytest.fixture, relative_file_path: str, is_exists: bool = True):
    project_basepath = Path(".")
    path_name = real_repository_name + "/" + relative_file_path

    assert project_basepath.joinpath(path_name).exists() == is_exists
    if is_exists:
        assert project_basepath.joinpath(path_name).is_file()


@then("The generated parent directory is named <real_repository_name>")
def check_project_parent_directory(context_dict, real_repository_name):
    check_if_directory(real_repository_name)


@then("The package subdirectory is named <real_package_name>")
def check_project_package_directory(real_repository_name, real_package_name):
    check_if_directory(real_repository_name, real_package_name)


@then("The documentation subdirectory is named docs")
def check_documentation_directory(real_repository_name):
    check_if_directory(real_repository_name, "docs")


@then("The tests subdirectory is named tests")
def check_tests_directory(real_repository_name):
    check_if_directory(real_repository_name, "tests")


@then("The package subdirectory contains an empty subdirectory named resources")
def check_package_resources_directory(real_repository_name, real_package_name):
    check_if_directory(real_repository_name, real_package_name + "/resources")


@then("The scripts subdirectory is named scripts")
def check_scripts_directory(real_repository_name):
    check_if_directory(real_repository_name, "scripts")


@then("The package subdirectory contains __init__.py file")
def check_package_init_file(real_repository_name, real_package_name):
    check_if_file(real_repository_name, real_package_name + "/__init__.py")


@then("The package subdirectory contains __main__.py file = <is_executable_package>")
def check_package_main_file(real_repository_name, real_package_name, is_executable_package):
    check_if_file(
        real_repository_name,
        real_package_name + "/__main__.py",
        is_exists=is_executable_package == "Yes")

@then("The repository has an README.rst file")
def check_readme_file(real_repository_name):
    check_if_file(real_repository_name, "README.rst")
