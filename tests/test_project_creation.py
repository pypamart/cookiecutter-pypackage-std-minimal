import os
import shutil
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter
from pytest_bdd import given, scenario, scenarios, then, when


@pytest.fixture(scope="module")
def dirpaths(tmp_path_factory):
    """
    Create an empty working directory
    """
    empty_working_directory = tmp_path_factory.getbasetemp()
    template_dirpath = Path.cwd()
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
        real_package_name=str)

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
def configure_context_repository_name(context_package_name, context_dict):
    if context_package_name:
        context_dict["package_name"] = context_package_name


@when("I generate my project structure with this extra context")
def bake_with_extra_context(dirpaths, context_dict):
    cookiecutter(
        dirpaths["template"].as_posix(),
        extra_context=context_dict,
        no_input=True,
        overwrite_if_exists=True)


@then("The generated parent directory is named <real_repository_name>")
def check_project_default_structure_in_working_dir(context_dict, real_repository_name):
    project_basepath = Path(".")

    # Assert
    assert project_basepath.joinpath(real_repository_name).exists()
    assert project_basepath.joinpath(real_repository_name).is_dir()


@then("The package subdirectory is named <real_package_name>")
def check_project_default_structure_in_working_dir(real_repository_name, real_package_name):
    project_basepath = Path(".")

    # Assert
    path_name = real_repository_name + "/" + real_package_name

    assert project_basepath.joinpath(path_name).exists()
    assert project_basepath.joinpath(path_name).is_dir()
