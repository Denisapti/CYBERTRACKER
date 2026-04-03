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
    
    # Resolve candidate data dirs.
    scanner_data_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scanner", "data"))
    data_dir = None

    # Make sure scanner data directory exists, even if repository ignored data files
    if not os.path.isdir(scanner_data_dir):
        os.makedirs(scanner_data_dir, exist_ok=True)

    # If the source data directory has hashes ready, use it
    if os.path.exists(os.path.join(scanner_data_dir, "hashes.csv")):
        data_dir = scanner_data_dir

    user_data_dir = None
    try:
        from scanner.paths import get_user_data_dir
        user_data_dir = get_user_data_dir()
    except Exception:
        user_data_dir = None

    if data_dir is None and user_data_dir:
        # Use AppData cache if available
        if os.path.exists(os.path.join(user_data_dir, "hashes.csv")):
            data_dir = user_data_dir

    if data_dir is None:
        # No data anywhere, attempt to bootstrap via update_hashes
        print("Data not found in scanner/data or AppData; attempting to download/initialize data...")
        try:
            from scanner.update_hashes import main as update_hashes_main
            update_hashes_main(force=True)
            if user_data_dir and os.path.exists(os.path.join(user_data_dir, "hashes.csv")):
                data_dir = user_data_dir
                print(f"Downloaded data into: {data_dir}")
        except Exception as e:
            print(f"Failed to download data during build bootstrap: {e}")

    # If we have AppData data but scanner/data path is empty, mirror it for bundling
    if data_dir and data_dir != scanner_data_dir:
        src_csv = os.path.join(data_dir, "hashes.csv")
        src_meta = os.path.join(data_dir, "metadata.json")
        if os.path.exists(src_csv):
            shutil.copy2(src_csv, os.path.join(scanner_data_dir, "hashes.csv"))
        if os.path.exists(src_meta):
            shutil.copy2(src_meta, os.path.join(scanner_data_dir, "metadata.json"))
        data_dir = scanner_data_dir
        print(f"Resolved data dir for bundling: {data_dir}")

    if data_dir is None:
        raise FileNotFoundError("Unable to locate or generate scanner data (hashes.csv, metadata.json).")

    if sys.platform == "win32":
        add_data_value = f"{data_dir};data"
    else:
        add_data_value = f"{data_dir}:data"

    add_data_args = ["--add-data", add_data_value]

    cmd.extend([
        "--clean",                    # Remove temporary files from previous builds
        *add_data_args,
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
