#!/usr/bin/env python3
"""
Build script for packaging CYBERTRACKER as a standalone executable.
Run this on Windows to generate the .exe file.

Usage:
    python build.py
"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """Build the executable using PyInstaller."""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "-q"], check=True)
    
    print("Building CYBERTRACKER executable...")
    
    # PyInstaller command
    # --onedir: creates folder with .exe and dependencies (cleaner for writable data)
    # --windowed: no console window
    # --add-data: bundle the data folder with read-only files
    # --name: output executable name
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",                                    # Folder build (better than --onefile)
        "--windowed",                                  # No console window
        "--name", "CYBERTRACKER",                     # Executable name
    ]
    
    # Add icon if it exists
    icon_path = "scanner/icon.ico"
    if os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
    
    # Add remaining arguments
    data_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scanner", "data"))
    if sys.platform == "win32":
        add_data_value = f"{data_path};data"
    else:
        add_data_value = f"{data_path}:data"

    cmd.extend([
        "--clean",                    # Remove temporary files from previous builds
        "--add-data", add_data_value,  # Bundle data
        "--collect-all", "pefile",   # Include pefile module
        "scanner/main.py"              # Main entry point
    ])
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    
    if result.returncode == 0:
        print("\n✓ Build successful!")
        print(f"\nExecutable created at: dist/CYBERTRACKER/main.exe")
        print("\nNext steps:")
        print("1. Test the executable: dist/CYBERTRACKER/main.exe <test_file>")
        print("2. Create registry file to add context menu")
        print("3. Double-click the .reg file to integrate with Windows")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    # Must be run on Windows or with PyInstaller cross-compilation support
    if sys.platform != "win32":
        print("Warning: PyInstaller builds are platform-specific.")
        print("Run this script on Windows to generate a Windows .exe file.")
        print("Proceeding anyway (may not work as expected)...\n")
    
    build_executable()
