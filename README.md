# UniRun

> **"Run Anything. Anywhere."**

UniRun is an open-source Universal Application Runtime orchestration layer designed to make software execution completely transparent and uniform across Linux systems. 

Users should focus on their applications, not on compatibility layers, runtimes, underlying execution engines, or fragmented package formats.

---

## Vision & Mission

### The Problem
Modern computing is highly fragmented. To run applications, users are constantly expected to navigate platform walls:
* Windows Apps $\rightarrow$ Managed manually via complex Wine/Proton prefixes.
* Android Apps $\rightarrow$ Instantiated via Waydroid environments.
* Linux Binaries $\rightarrow$ Sandboxed via AppImages, Flatpaks, or native package managers.
* Web Apps $\rightarrow$ Dispatched into standalone browser engines or Electron instances.

This imposes an unnecessary cognitive load. 

### Our Mission
UniRun aims to abstract and hide this entire layer of complexity. By providing a smart unified interface, UniRun dynamically evaluates, intercepts, and provisions dependencies out-of-the-box. Instead of running system-specific syntax like `wine setup.exe` or `waydroid app install game.apk`, users run one universal workflow command:
```bash
unirun run application

UniRun instantly routes execution to the optimal ecosystem backend.
🛠️ Commands & Usage

UniRun offers an intuitive CLI layout supporting explicit runtime commands or a complete direct interception engine:
Core CLI Registry

    unirun run <file> — Explicitly analyzes and invokes the appropriate backend layer for a given binary, script, package, or URL.

    unirun doctor — Diagnoses your system environment status and reports on dependencies (Wine, Waydroid, XDG utils, etc.).

    unirun history — View the local runtime execution logs of previously launched programs.

    unirun version — Displays the current software release variant.

    unirun help — Interactive command layout utility.

Automatic Execution (Direct Launch)

You can completely omit the run argument! Passing any local path, configuration index, global application token, or network link directly to UniRun causes it to intercept, target evaluate, and execute instantly.
Bash

unirun setup.exe            # Instantly provisions target via Wine
unirun mobile_game.apk      # Hands off standalone sandbox execution to Waydroid
unirun application.AppImage # Mounts and dispatches standalone immutable bundle
unirun firefox              # Seamlessly launches native desktop environment binaries
unirun search minecraft     # Discovers and locates local asset configurations across partitions
unirun [https://google.com](https://google.com)   # Identifies web target and routes natively via Web Engine

Future Roadmap

    v0.3 (Current): Core interception layer, explicit/implicit CLI parsing paths, standard desktop environment integrations.

    v0.4: Compatibility Rating Matrix (inspired by ProtonDB), incorporating direct community ratings and custom runner profiles.

    v0.5: Self-healing auto-configuration layer (automatic missing package manager checks, sandboxed prefix management, seamless Waydroid initialization scripts).

    Long-Term Target: Global Cross-Platform abstraction covering x86_64, ARM64, and RISC-V architectures uniformly.

LICENSE:

MIT

CREATOR:

KASISH