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
    """Build the executable using PyInstaller.
    
    Data files (hashes.csv, database.db) are NOT bundled.
    They will be downloaded/initialized on first run by the application.
    """
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "-q"], check=True)
    
    print("Building CYBERTRACKER executable...")
    print("(Data files will be downloaded on first run)\n")
    
    # PyInstaller command
    # --onedir: folder build with .exe and dependencies in separate folder
    # --windowed: no console window on startup
    # --clean: remove old build artifacts
    # --collect-all pefile: bundle the pefile module completely
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",                    # Folder build (cleaner, keeps deps separate)
        "--windowed",                  # No console window
        "--name", "CYBERTRACKER",      # Output executable name
        "--clean",                     # Remove old build files
        "--collect-all", "pefile",     # Include pefile module and dependencies
        "--hidden-import=requests",    # Explicitly include requests module
        "scanner/main.py"              # Entry point
    ]
    
    print(f"Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    
    if result.returncode == 0:
        print("\n✓ Build successful!")
        print(f"\nExecutable created at: dist/CYBERTRACKER/main.exe")
        print("\n📋 Next steps:")
        print("1. First run: main.exe will download malware data from MalwareBazaar (~100-200MB)")
        print("   This creates files in: %APPDATA%\\CYBERTRACKER\\")
        print("2. Generate context menu: python generate_context_menu.py")
        print("3. Install: Double-click install_context_menu.reg")
        print("4. Use: Right-click any file → 'Scan with CYBERTRACKER'")
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
