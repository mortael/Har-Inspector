# HAR Inspector Desktop (Python)

This folder contains a Python desktop version of the HAR Inspector UI, built with `customtkinter` for a small distributable.

## Run (dev)

```bash
cd desktop
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -U pip
python -m pip install -e .
python -m har_inspector_desktop
```

## CLI validation (headless)

```bash
python -m har_inspector_desktop --validate path/to/file.har
```

## Build Windows EXE (PyInstaller)

```powershell
cd desktop
py -m pip install -e .
py -m pip install ".[build]"
./scripts/build_windows.ps1
```

The output EXE is created in `desktop/dist/HarInspector.exe`.

Size tips:

- Use `--onefile` and `--noconsole` (already configured).
- If you have UPX installed, PyInstaller will automatically compress compatible binaries.

## Create Windows installer (Inno Setup)

1. Install Inno Setup.
2. Build the EXE (above).
3. Open `desktop/installer/windows/HarInspector.iss` in Inno Setup and build.
