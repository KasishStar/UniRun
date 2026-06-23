# UniRun

> **Run Anything. Anywhere.**

UniRun is a universal application runtime orchestration layer for Linux. It automatically detects what kind of file you're trying to run and routes it to the correct runtime — no more remembering `wine`, `waydroid`, `xdg-open`, or `chmod +x`.

```bash
unirun setup.exe              # Automatically runs via Wine
unirun game.apk                # Installs via Waydroid
unirun app.AppImage            # Makes executable and launches
unirun document.pdf            # Opens with system default
unirun firefox                 # Finds and launches system binary
unirun https://example.com     # Opens in browser
```

## Install

### PyPI (recommended)
```bash
pip install unirun
```

### Arch Linux (AUR)
```bash
yay -S unirun-git
```

### From Source
```bash
git clone https://github.com/KasishStar/UniRun.git
cd UniRun
pip install -e .
```

## Usage

```
unirun <command> [arguments]
unirun <file_path_or_command_name>
```

### Commands

| Command | Description |
|---------|-------------|
| `run <file>` | Explicitly run a file with auto-detected runtime |
| `search <query>` | Search filesystem for matching files |
| `install <package>` | Install a runtime or package |
| `doctor` | Check installed runtimes status |
| `history` | Show recently launched files |
| `config` | Show current configuration |
| `version` | Show version |
| `help` | Show help |

### Options

| Flag | Description |
|------|-------------|
| `--verbose, -v` | Enable detailed logging |

### Direct Launch

You can skip the `run` command entirely:

```bash
unirun setup.exe
unirun game.apk
unirun firefox
```

## Configuration

Config file: `~/.config/unirun/config.json`

```json
{
  "search_dirs": ["~/Downloads", "~/Documents"],
  "history_file": "~/.local/share/unirun/history.log"
}
```

Set `UNIRUN_CONFIG` environment variable for a custom config path.

## How It Works

1. **Detect** — UniRun checks the file extension and type
2. **Route** — It hands off to the correct runtime:
   - `.exe`, `.msi` → Wine
   - `.apk` → Waydroid
   - `.AppImage` → Native execution
   - `.pdf`, `.png`, `.mp4`, `.mp3`, etc. → XDG default app
   - `http://`, `https://` → Web browser
   - Everything else → Native execution
3. **Fallback** — If the file isn't found, UniRun searches common directories

## Supported Runtimes

- **Wine** — Windows executables
- **Waydroid** — Android applications
- **AppImage** — Portable Linux packages
- **XDG** — Documents, images, videos, audio
- **Native** — System binaries and scripts
- **Web** — URLs opened in browser

## Development

```bash
git clone https://github.com/KasishStar/UniRun.git
cd UniRun
pip install -e .
python tests/test_all.py
```

## License

MIT — Created by Kasish
