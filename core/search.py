from pathlib import Path


SEARCH_DIRS = [
    Path.home() / "Downloads",
    Path.home() / "Documents",
    Path.home() / "Pictures",
    Path.home() / "Videos",
    Path.home() / "Desktop"
]


def find_file(filename):

    for directory in SEARCH_DIRS:

        if not directory.exists():
            continue

        for file in directory.rglob("*"):

            if file.name.lower() == filename.lower():
                return str(file)

    return None