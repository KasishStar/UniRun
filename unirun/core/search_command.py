import os
from unirun.core.search import get_search_dirs

def search_files(query, raw=False):
    results = []
    query = query.lower()
    search_dirs = get_search_dirs()

    for directory in search_dirs:
        for root, dirs, files in os.walk(directory):
            for f in files:
                if query in f.lower():
                    results.append(os.path.join(root, f))
                    if len(results) >= 30:
                        break
            if len(results) >= 30:
                break

    if raw:
        return results

    if not results:
        print("[UniRun] No results found")
        return

    print(f"\nFound {len(results)} result(s):\n")
    for idx, result in enumerate(results, start=1):
        print(f"  {idx}. {result}")
    print()
