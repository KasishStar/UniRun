import os
from pathlib import Path
from unirun.config import load_config

def get_search_dirs():
    cfg = load_config()
    dirs = cfg.get("search_dirs", [])
    expanded = []
    for d in dirs:
        d = os.path.expanduser(d)
        if os.path.isdir(d):
            expanded.append(d)
    # Always include home dirs as fallback
    home = Path.home()
    for sub in ["Downloads", "Documents", "Pictures", "Desktop", "Videos", "Music"]:
        p = home / sub
        if p.is_dir() and str(p) not in expanded:
            expanded.append(str(p))
    return expanded

def find_file(filename):
    search_dirs = get_search_dirs()
    for directory in search_dirs:
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.lower() == filename.lower():
                    return os.path.join(root, f)
    return None

def fuzzy_find(query, max_results=5):
    search_dirs = get_search_dirs()
    query = query.lower()
    results = []

    for directory in search_dirs:
        for root, dirs, files in os.walk(directory):
            for f in files:
                name_lower = f.lower()
                # Substring match
                if query in name_lower:
                    results.append((10, os.path.join(root, f)))
                # Fuzzy char match
                elif all(c in name_lower for c in query):
                    results.append((5, os.path.join(root, f)))

    results.sort(key=lambda x: -x[0])
    seen = set()
    unique = []
    for score, path in results:
        if path not in seen:
            seen.add(path)
            unique.append(path)

    if not unique:
        return None

    return unique[0] if max_results == 1 else unique[:max_results]
