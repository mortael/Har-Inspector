# HAR Inspector (Desktop)

HAR Inspector is now a Python desktop app built with **customtkinter**.

## Features

- Open `.har` / `.json` HAR files locally
- Filter entries by URL and HTTP method
- Inspect full entry details
- Edit URL, method, and response status for any entry
- Remove selected entries
- Save modified HAR files
- Export filtered rows to CSV

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-desktop.txt
python desktop_app.py
```

## Build Windows EXE (small single-file build)

```bash
pip install -r requirements-desktop.txt
pyinstaller --clean --noconfirm har_inspector_desktop.spec
```

Output binary: `dist/har-inspector.exe`

## Build Windows installer

Use [Inno Setup](https://jrsoftware.org/isinfo.php) with:

```text
installer_windows.iss
```

Output installer: `dist/har-inspector-setup.exe`
