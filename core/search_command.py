from pathlib import Path


SEARCH_DIRS = [
    Path.home() / "Downloads",
    Path.home() / "Documents",
    Path.home() / "Pictures",
    Path.home() / "Desktop",
    Path.home() / "Videos"
]


def search_files(query):

    results = []

    query = query.lower()

    for directory in SEARCH_DIRS:

        if not directory.exists():
            continue

        for file in directory.rglob("*"):

            if query in file.name.lower():

                results.append(str(file))

                if len(results) >= 20:
                    break

    if not results:
        print("[UniRun] No results found")
        return

    print("\nFound:\n")

    for index, result in enumerate(results, start=1):
        print(f"{index}. {result}")