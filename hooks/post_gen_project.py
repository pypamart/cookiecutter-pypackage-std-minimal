from pathlib import Path


def remove_gitkeep_files(): 
    """
    Remove .gitkeep files that serve to archive empty folders with git.
    """
    gitkeep_files = [path for path in Path('.').glob('**/.gitkeep')]

    for path in gitkeep_files:
        path.unlink()


if __name__ == '__main__':
    remove_gitkeep_files()

    if '{{ cookiecutter.is_executable_package }}' == 'No':
        Path('./{{ cookiecutter.package_name }}/__main__.py').unlink()
        

