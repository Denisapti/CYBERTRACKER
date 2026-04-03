#!/usr/bin/env python3
"""
Generate the Windows registry file for context menu integration.
This script creates a .reg file with the correct path to the CYBERTRACKER executable.

Usage:
    python generate_context_menu.py [path_to_executable]
    
    If no path provided, will look for CYBERTRACKER in dist/ folder.
"""

import os
import sys
import subprocess

def generate_reg_file(exe_path):
    """
    Generate and return the registry file content for the given executable path.
    """
    # Escape backslashes for registry
    reg_path = exe_path.replace("\\", "\\\\")
    
    reg_content = f"""Windows Registry Editor Version 5.00

; Context menu entry for CYBERTRACKER malware scanner
; Generated automatically - do not edit manually

[HKEY_CLASSES_ROOT\\*\\shell\\ScanWithCYBERTRACKER]
@="Scan with CYBERTRACKER"

[HKEY_CLASSES_ROOT\\*\\shell\\ScanWithCYBERTRACKER\\command]
@="\\"{reg_path}\\" \\"%1\\""
"""
    return reg_content

def find_executable():
    """Try to find the CYBERTRACKER executable."""
    candidates = [
        "dist/CYBERTRACKER/main.exe",
        os.path.join(os.path.dirname(__file__), "dist", "CYBERTRACKER", "main.exe"),
    ]
    
    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)
    
    return None

def main():
    # Determine executable path
    if len(sys.argv) > 1:
        exe_path = sys.argv[1]
    else:
        exe_path = find_executable()
        if not exe_path:
            print("Error: Could not find CYBERTRACKER executable.")
            print("Usage: python generate_context_menu.py [path_to_main.exe]")
            print("\nOr build it first with: python build.py")
            sys.exit(1)
    
    # Verify executable exists
    if not os.path.exists(exe_path):
        print(f"Error: Executable not found at {exe_path}")
        sys.exit(1)
    
    exe_path = os.path.abspath(exe_path)
    
    # Generate registry file
    reg_content = generate_reg_file(exe_path)
    
    # Write to file
    output_file = "install_context_menu.reg"
    with open(output_file, "w") as f:
        f.write(reg_content)
    
    print(f"✓ Generated: {output_file}")
    print(f"\nNext steps:")
    print(f"1. Double-click {output_file}")
    print(f"2. Click 'Yes' when prompted by Windows")
    print(f"3. Right-click any file and select 'Scan with CYBERTRACKER'")
    print(f"\nTo remove the context menu entry later:")
    print(f"- Run: reg delete HKEY_CLASSES_ROOT\\*\\shell\\ScanWithCYBERTRACKER /f")

if __name__ == "__main__":
    main()
