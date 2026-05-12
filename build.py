"""
Build script for creating HAR Inspector executable
Creates a standalone .exe file with PyInstaller
"""

import PyInstaller.__main__
import sys
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(script_dir, 'har_inspector.py')

# PyInstaller arguments
args = [
    app_path,
    '--name=HARInspector',
    '--onefile',  # Create a single executable file
    '--windowed',  # No console window (GUI only)
    '--clean',  # Clean PyInstaller cache
    '--noconfirm',  # Replace output directory without asking

    # Optimization options
    '--strip',  # Strip symbols (Linux/Mac only, ignored on Windows)
    '--noupx',  # Don't use UPX (can sometimes cause issues)

    # Icon (optional - would need an icon file)
    # '--icon=icon.ico',

    # Hidden imports (if needed)
    '--hidden-import=customtkinter',
    '--hidden-import=PIL',
    '--hidden-import=PIL._tkinter_finder',

    # Collect data files
    '--collect-data=customtkinter',

    # Exclude unnecessary modules to reduce size
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--exclude-module=pandas',
    '--exclude-module=scipy',
    '--exclude-module=pytest',
    '--exclude-module=unittest',
]

print("Building HAR Inspector executable...")
print("This may take a few minutes...")

try:
    PyInstaller.__main__.run(args)
    print("\n" + "="*60)
    print("Build complete!")
    print("Executable location: dist/HARInspector.exe (Windows) or dist/HARInspector (Linux/Mac)")
    print("="*60)
except Exception as e:
    print(f"\nBuild failed: {e}", file=sys.stderr)
    sys.exit(1)
