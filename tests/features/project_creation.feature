Feature: Project creation
  In order to start my new project as a developper, I want to generate a project structure from a cookiecutter template

  Scenario Outline: Project creation
    Given I am in a working project directory
    When I configure the repository name as <context_repository_name> in the extra context
    And I configure the package name as <context_package_name> in the extra context
    And I configure the package as executable = <is_executable_package>
    And I generate my project structure with this extra context
    Then The generated parent directory is named <real_repository_name>
    And The package subdirectory is named <real_package_name>
    And The package subdirectory contains an empty subdirectory named resources
    And The package subdirectory contains __init__.py file
    And The package subdirectory contains __main__.py file = <is_executable_package>
    And The documentation subdirectory is named docs
    And The tests subdirectory is named tests
    And The scripts subdirectory is named scripts
    And The repository has an README.rst file


    Examples:
      | context_repository_name        | context_package_name | real_repository_name           | real_package_name            | is_executable_package |
      |                                |                      | package_name[-subpackage_name] | package_name_subpackage_name | No                    |
      | Package_Name[-Subpackage_Name] |                      | Package_Name[-Subpackage_Name] | package_name_subpackage_name | Yes                   |
      |                                | my_package           | package_name[-subpackage_name] | my_package                   | No                    |
      | My Repository                  | my_package           | My Repository                  | my_package                   | Yes                   |



