import os
import sys
import shutil
import subprocess
import tempfile

# Comprehensive global abstraction registry mapping generic inputs to explicit targets
PACKAGE_REGISTRY = {
    "wine": {"type": "pacman", "target": "wine"},
    "steam": {"type": "pacman", "target": "steam"},
    "waydroid": {"type": "pacman", "target": "waydroid"},
    "git": {"type": "pacman", "target": "git"},
    "python": {"type": "pacman", "target": "python"},
    "lutris": {"type": "pacman", "target": "lutris"},
    "bottles": {"type": "pacman", "target": "bottles"},
    "java": {"type": "pacman", "target": "jdk-openjdk"},
    "flatpak": {"type": "pacman", "target": "flatpak"},
    "electron": {"type": "pacman", "target": "electron"},
    
    # AUR Exclusives (Built natively via Git & makepkg)
    "proton": {"type": "aur", "target": "protonup-cli"},
    "protonup-qt": {"type": "aur", "target": "protonup-qt"},
    "heroic": {"type": "aur", "target": "heroic-games-launcher-bin"},
    "minecraft-launcher": {"type": "aur", "target": "minecraft-launcher"},
}

def build_aur_package(package_name):
    """
    Clones an AUR package repository into a temporary workspace,
    resolves internal configuration, and executes a native makepkg compilation.
    """
    print(f"[UniRun] SOURCE: Arch User Repository (AUR) [Community Source Tree]")
    print(f"[UniRun] STATUS: Initializing native compilation pipeline for '{package_name}'...")
    
    # Verify build requirements are present on the host shell
    for tool in ["git", "makepkg"]:
        if not shutil.which(tool):
            print(f"[UniRun] ERROR: Required compilation dependency missing from host system environment: '{tool}'")
            return False

    # Create an isolated temporary staging directory for building
    with tempfile.TemporaryDirectory() as tmpdir:
        clone_url = f"https://aur.archlinux.org/{package_name}.git"
        repo_dir = os.path.join(tmpdir, package_name)
        
        print(f"[UniRun] DOWNLOADING: Fetching remote source tree from {clone_url}...")
        try:
            subprocess.run(["git", "clone", clone_url, repo_dir], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f"[UniRun] ERROR: Failed to clone target AUR repository mapping.")
            return False

        print(f"[UniRun] COMPILING: Executing source compilation and dependency resolution via makepkg...")
        try:
            # -s installs missing dependencies via pacman automatically
            # -i installs the resulting package on the host system
            # --noconfirm ensures hands-off headless automated running
            subprocess.run(
                ["makepkg", "-si", "--noconfirm"],
                cwd=repo_dir,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            print(f"[UniRun] ERROR: Native AUR compilation failed during package generation phase.")
            return False

def install_package(name):
    query = name.lower()

    # 1. Detect if it's an explicit flatpak application ID structure (e.g., com.example.App)
    if query.count('.') >= 2 or query.startswith("org.") or query.startswith("com."):
        print(f"[UniRun] SOURCE: Flathub Remote Registry [Flatpak Sandboxed Container]")
        print(f"[UniRun] STATUS: Preparing deployment matrix for sandboxed application: '{name}'")
        
        if not shutil.which("flatpak"):
            print("[UniRun] DEPENDENCY: Flatpak system subsystem missing. Provisioning system layer first via pacman...")
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "flatpak"])
        
        print(f"[UniRun] RUNNING: Passing transaction stream to Flatpak backend runtime...")
        subprocess.run(["flatpak", "install", "flathub", name, "-y"])
        print(f"[UniRun] SUCCESS: Application package '{name}' deployed securely inside Flatpak environment.")
        return

    # 2. Match against global abstraction table records
    pkg_meta = PACKAGE_REGISTRY.get(query)
    
    if not pkg_meta:
        # Dynamic Fallback: If not registered, assume it's a raw Pacman target request
        print(f"[UniRun] SOURCE: Fallback System Matching Engine")
        print(f"[UniRun] WARN: Package Reference '{name}' unlisted in local records. Assuming official pacman target...")
        pkg_meta = {"type": "pacman", "target": name}

    target = pkg_meta["target"]

    if pkg_meta["type"] == "pacman":
        print(f"[UniRun] SOURCE: Arch Linux Core Repositories [Official Upstream Binaries]")
        print(f"[UniRun] STATUS: Targeting standard package manager index allocation for -> '{target}'")
        try:
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", target], check=True)
            print(f"[UniRun] SUCCESS: Package '{target}' successfully deployed to host system natively.")
        except subprocess.CalledProcessError:
            # Ultimate fail-safe: If pacman fails, check if it's an unmapped AUR package!
            print(f"[UniRun] WARN: Upstream database lookup failed. Diverting target to dynamic AUR builder tracking...")
            success = build_aur_package(target)
            if success:
                print(f"[UniRun] SUCCESS: Package '{target}' deployed successfully via fallback build matrix.")

    elif pkg_meta["type"] == "aur":
        success = build_aur_package(target)
        if success:
            print(f"[UniRun] SUCCESS: Automated AUR deployment routine verified for system package '{target}'.")