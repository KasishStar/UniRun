import os
from pathlib import Path
from unirun.ui import format_size

DOCUMENTS = {".pdf", ".txt", ".md", ".csv", ".json", ".xml", ".html"}
IMAGES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp"}
VIDEOS = {".mp4", ".mkv", ".webm", ".avi", ".mov", ".flv"}
AUDIO = {".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a"}
ARCHIVES = {".zip", ".tar", ".gz", ".bz2", ".xz", ".rar", ".7z"}
CODES = {".py", ".sh", ".js", ".ts", ".rs", ".go", ".c", ".cpp", ".h", ".rb", ".java", ".swift"}

RUNTIME_MAP = {
    ".exe": "windows", ".msi": "windows",
    ".apk": "android",
    ".appimage": "appimage",
}

TYPE_NAMES = {
    ".exe": "Windows Executable", ".msi": "Windows Installer",
    ".apk": "Android Package",
    ".appimage": "AppImage",
    ".pdf": "PDF Document", ".txt": "Text File", ".md": "Markdown",
    ".csv": "CSV Spreadsheet", ".json": "JSON Data", ".xml": "XML Data",
    ".png": "PNG Image", ".jpg": "JPEG Image", ".jpeg": "JPEG Image",
    ".webp": "WebP Image", ".gif": "GIF Image", ".svg": "SVG Vector",
    ".mp4": "MP4 Video", ".mkv": "MKV Video", ".webm": "WebM Video",
    ".avi": "AVI Video", ".mov": "MOV Video",
    ".mp3": "MP3 Audio", ".wav": "WAV Audio", ".flac": "FLAC Audio",
    ".ogg": "OGG Audio", ".aac": "AAC Audio",
    ".zip": "ZIP Archive", ".tar": "TAR Archive",
    ".rar": "RAR Archive",     ".7z": "7-Zip Archive",
    ".py": "Python Script", ".sh": "Shell Script", ".js": "JavaScript",
    ".ts": "TypeScript", ".rs": "Rust Source", ".go": "Go Source",
    ".c": "C Source", ".cpp": "C++ Source", ".h": "C Header",
    ".rb": "Ruby Script", ".java": "Java Source", ".swift": "Swift Source",
    ".jar": "Java Archive",
}

def detect(filepath):
    if filepath.startswith("http://") or filepath.startswith("https://"):
        return "web"

    ext = Path(filepath).suffix.lower()
    if ext in RUNTIME_MAP:
        return RUNTIME_MAP[ext]
    if ext in DOCUMENTS | IMAGES | VIDEOS | AUDIO | ARCHIVES:
        return "xdg"
    return "native"

def get_file_info(filepath):
    ext = Path(filepath).suffix.lower()
    runtime = detect(filepath)
    type_name = TYPE_NAMES.get(ext, "Unknown")

    if filepath.startswith("http://") or filepath.startswith("https://"):
        return {
            "ext": "",
            "runtime": "web",
            "type_name": "Web URL",
            "size": None,
            "executable": None,
        }

    if not os.path.exists(filepath):
        return {"ext": ext, "runtime": runtime, "type_name": type_name, "size": None, "executable": None}

    stat = os.stat(filepath)
    size = format_size(stat.st_size) if stat.st_size >= 0 else None

    if os.path.isdir(filepath):
        return {
            "ext": "",
            "runtime": "xdg",
            "type_name": "Directory",
            "size": None,
            "executable": None,
        }

    is_exec = os.access(filepath, os.X_OK) if not os.path.isdir(filepath) else None

    return {
        "ext": ext,
        "runtime": runtime,
        "type_name": type_name,
        "size": size,
        "executable": is_exec,
    }
