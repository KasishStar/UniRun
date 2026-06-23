import shutil
import os

class C:
    RST = "\033[0m"
    BLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GRN = "\033[32m"
    YLW = "\033[33m"
    BLU = "\033[34m"
    MAG = "\033[35m"
    CYN = "\033[36m"
    LRED = "\033[91m"
    LGRN = "\033[92m"
    LYLW = "\033[93m"

def ok(text):
    return f"{C.GRN}✓ {text}{C.RST}"

def fail(text):
    return f"{C.RED}✗ {text}{C.RST}"

def warn(text):
    return f"{C.YLW}⚠ {text}{C.RST}"

def info(text):
    return f"{C.BLU}ℹ {text}{C.RST}"

def bold(text):
    return f"{C.BLD}{text}{C.RST}"

def dim(text):
    return f"{C.DIM}{text}{C.RST}"

def header(text):
    w = shutil.get_terminal_size().columns
    return f"\n{C.BLD}{text}{C.RST}\n{C.DIM}{'═' * min(len(text) + 2, w)}{C.RST}"

def subheader(text):
    return f"  {C.BLD}{text}{C.RST}"

def runtime_badge(runtime):
    colors = {
        "windows": C.CYN, "android": C.GRN, "appimage": C.MAG,
        "web": C.BLU, "xdg": C.YLW, "native": C.LGRN,
    }
    color = colors.get(runtime, C.RST)
    return f"{color}[{runtime.upper()}]{C.RST}"

def confirm(msg, default=True):
    suffix = " [Y/n]" if default else " [y/N]"
    prompt = f"  {C.YLW}?{C.RST} {msg}{suffix} "
    try:
        resp = input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return default
    if default:
        return resp not in ("n", "no")
    return resp in ("y", "yes")

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
