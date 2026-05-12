#!/usr/bin/env python3
"""
Quick start script for HAR Inspector
Checks dependencies and launches the application
"""

import sys
import subprocess
import importlib.util

def check_dependency(package_name, install_name=None):
    """Check if a package is installed"""
    if install_name is None:
        install_name = package_name

    spec = importlib.util.find_spec(package_name)
    return spec is not None

def main():
    print("HAR Inspector - Starting up...\n")

    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)

    print(f"✓ Python version: {sys.version.split()[0]}")

    # Check dependencies
    dependencies = {
        'customtkinter': 'customtkinter',
        'PIL': 'Pillow',
        'tkinter': 'tkinter (built-in)'
    }

    missing = []
    for package, install_name in dependencies.items():
        if check_dependency(package):
            print(f"✓ {install_name}")
        else:
            print(f"✗ {install_name} - MISSING")
            missing.append(install_name)

    if missing:
        print("\nMissing dependencies detected!")
        print("Please install them using:")
        print(f"  pip install -r requirements.txt")
        print("\nOr install individually:")
        for dep in missing:
            if dep != 'tkinter (built-in)':
                print(f"  pip install {dep}")
        sys.exit(1)

    print("\n✓ All dependencies satisfied")
    print("Launching HAR Inspector...\n")

    # Launch the application
    try:
        import har_inspector
        har_inspector.main()
    except Exception as e:
        print(f"\nERROR: Failed to launch application")
        print(f"Details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
