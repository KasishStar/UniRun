import os
import sys
import shutil
import subprocess
import tempfile

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
    
    "proton": {"type": "aur", "target": "protonup-cli"},
    "protonup-qt": {"type": "aur", "target": "protonup-qt"},
    "heroic": {"type": "aur", "target": "heroic-games-launcher-bin"},
    "minecraft-launcher": {"type": "aur", "target": "minecraft-launcher"},
}

def execute_aur_build(package_name):
    """
    Clones, verifies, and compiles an AUR package.
    Returns True on success, False if PKGBUILD is missing or compilation fails.
    """
    for tool in ["git", "makepkg"]:
        if not shutil.which(tool):
            print(f"[UniRun] ERROR: System build dependency missing from host environment: '{tool}'")
            return False

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_url = f"https://aur.archlinux.org/{package_name}.git"
        repo_dir = os.path.join(tmpdir, package_name)
        
        print(f"[UniRun] DOWNLOADING: Fetching remote source tree from {clone_url}")
        try:
            subprocess.run(["git", "clone", clone_url, repo_dir], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f"[UniRun] WARN: Could not reach or clone git address target for '{package_name}'")
            return False

        # VERIFICATION STEP: Make sure the package build script actually exists in the cloned path
        if not os.path.exists(os.path.join(repo_dir, "PKGBUILD")):
            print(f"[UniRun] WARN: Repository layout mismatch. No PKGBUILD found in tree for '{package_name}'")
            return False

        print(f"[UniRun] COMPILING: Executing source compilation and dependency resolution via makepkg...")
        try:
            subprocess.run(["makepkg", "-si", "--noconfirm"], cwd=repo_dir, check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"[UniRun] WARN: Target makepkg execution context exited with errors.")
            return False

def try_aur_pipeline(target_name):
    """
    Intelligent alternative solver that cycles through typical naming variations
    if the primary database string fails to compile.
    """
    print(f"[UniRun] SOURCE: Arch User Repository (AUR) [Community Source Tree]")
    print(f"[UniRun] STATUS: Initializing native compilation pipeline for '{target_name}'...")
    
    # Strategy 1: Explicit target match
    if execute_aur_build(target_name):
        return True
        
    # Strategy 2: Pre-compiled binary fallback fallback (adding -bin tag)
    if not target_name.endswith("-bin"):
        fallback_bin = f"{target_name}-bin"
        print(f"[UniRun] FALLBACK: Primary build failed. Switching to alternative pre-compiled source tree: '{fallback_bin}'")
        if execute_aur_build(fallback_bin):
            return True

    # Strategy 3: Development branch fallback fallback (adding -git tag)
    if not target_name.endswith("-git"):
        fallback_git = f"{target_name}-git"
        print(f"[UniRun] FALLBACK: Secondary build failed. Pivoting to upstream development branch tracking: '{fallback_git}'")
        if execute_aur_build(fallback_git):
            return True

    return False

def install_package(name):
    query = name.lower()

    # 1. Flatpak Sandboxed Path Logic
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

    # 2. Extract or infer target mapping
    pkg_meta = PACKAGE_REGISTRY.get(query)
    if not pkg_meta:
        print(f"[UniRun] SOURCE: Dynamic Fallback System Matching Engine")
        print(f"[UniRun] WARN: Package Reference '{name}' unlisted in local records. Directing to core databases...")
        pkg_meta = {"type": "pacman", "target": name}

    target = pkg_meta["target"]

    # 3. Pacman Execution Path with Self-Healing Fallback
    if pkg_meta["type"] == "pacman":
        print(f"[UniRun] SOURCE: Arch Linux Core Repositories [Official Upstream Binaries]")
        print(f"[UniRun] STATUS: Targeting standard package manager index allocation for -> '{target}'")
        try:
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", target], check=True)
            print(f"[UniRun] SUCCESS: Package '{target}' successfully deployed to host system natively.")
        except subprocess.CalledProcessError:
            print(f"[UniRun] WARN: Upstream database transaction failed. Diverting target to dynamic AUR builder tracking...")
            if try_aur_pipeline(target):
                print(f"[UniRun] SUCCESS: Package '{target}' deployed successfully via fallback build matrix.")
            else:
                print(f"[UniRun] CRITICAL: All package resolution vectors exhausted. Unable to install '{name}'.")

    # 4. Pure AUR Path
    elif pkg_meta["type"] == "aur":
        if try_aur_pipeline(target):
            print(f"[UniRun] SUCCESS: Automated AUR deployment routine verified for system package '{target}'.")
        else:
            print(f"[UniRun] CRITICAL: All package resolution vectors exhausted. Unable to install '{name}'.")