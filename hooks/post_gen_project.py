from pathlib import Path

def remove_gitkeep_files(): 
    """
    Remove .gitkeep files that serve to archive empty folders with git.
    """
    gitkeep_files = [path for path in Path('.').glob('**/.gitkeep')]

    for path in gitkeep_files:
        path.unlink()

remove_gitkeep_files()