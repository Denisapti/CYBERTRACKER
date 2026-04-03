# CYBERTRACKER - Windows Integration Installation Guide

This guide covers building and installing CYBERTRACKER as a Windows application with right-click context menu integration.

## Quick Start (For Windows Users)

### Step 1: Build the Executable

1. Ensure you have Python 3.8+ installed on Windows
2. Open Command Prompt and navigate to the CYBERTRACKER folder
3. Run:
   ```cmd
   python build.py
   ```
   This will create `dist/CYBERTRACKER/main.exe`

### Step 2: Add to Right-Click Menu

1. Run:
   ```cmd
   python generate_context_menu.py
   ```
   This creates `install_context_menu.reg`

2. Double-click `install_context_menu.reg`
3. Click "Yes" when Windows asks to modify the registry

### Step 3: Use It!

Right-click any file and select **"Scan with CYBERTRACKER"**
- A popup window will appear showing the scan results
- No console window, no buttons—just results

---

## What Gets Built

```
dist/
└── CYBERTRACKER/
    ├── main.exe                    (the application)
    ├── database.db                 (bundled template, read-only)
    ├── hashes.csv                  (bundled seed data)
    └── [other dependencies]
```

### First Run Behavior

On first use:
1. Creates `%APPDATA%\CYBERTRACKER\` folder
2. Copies database and CSV to that location
3. Initializes the malware signatures database

### Persistent Data

All user data is stored in `%APPDATA%\CYBERTRACKER\`:
- `database.db` — malware hashes (populated on first run, updated periodically)
- `hashes.csv` — cached malware signatures from MalwareBazaar
- `metadata.json` — timestamp of last update

This means:
- ✓ Data persists between runs
- ✓ Updates don't lose your database
- ✓ Follows Windows application conventions

---

## Manual Installation (If Needed)

If you prefer not to use the registry file:

1. Copy the `dist/CYBERTRACKER` folder to a permanent location (e.g., `C:\Program Files\CYBERTRACKER`)
2. Create a shortcut to `main.exe`
3. Right-click any file and select "Open with" → choose `main.exe`

---

## Command Line Usage (For Developers)

```bash
# Standard scan (shows popup on Windows, prints JSON on Linux)
python scanner/main.py <file_path>

# Show popup and print JSON
python scanner/main.py <file_path>

# CLI mode only (no UI popup, for scripting)
python scanner/main.py <file_path> --cli

# Force database update
python scanner/main.py <file_path> --force

# Combination
python scanner/main.py <file_path> --force --cli
```

---

## Troubleshooting

### "No registry changes. Access denied."
- Run Command Prompt as Administrator
- Double-click the .reg file with admin privileges

### Context menu entry doesn't appear
- Check that `main.exe` path in `.reg` file is correct
- Run `python generate_context_menu.py` again
- Log out and back in (or restart Windows)

### "Database needs to be updated!" on every scan
- First scan downloads/initializes the database—this is normal
- Subsequent scans should use cached data

### Application won't start
- Verify Python packages are installed: `pip install pefile requests`
- Check that `%APPDATA%\CYBERTRACKER\` folder has write permissions

---

## Architecture Overview

The application is structured to work offline-first:

1. **Bundled Data**: Initial seed data is packaged with the exe
2. **User Data Location**: `%APPDATA%\CYBERTRACKER\` persists across updates
3. **Online Lookup**: Periodically checks MalwareBazaar for updates
4. **Graceful Fallback**: Uses cached data if network is unavailable

The UI is intentionally minimal:
- ✓ No buttons or menus (just click to dismiss)
- ✓ Works via right-click integration
- ✓ Clear, color-coded results
- ✓ No console window

---

## Uninstalling

1. Delete the `dist/CYBERTRACKER` folder
2. Remove the registry entry by running:
   ```cmd
   reg delete HKEY_CLASSES_ROOT\*\shell\ScanWithCYBERTRACKER /f
   ```
   Or: Delete `%APPDATA%\CYBERTRACKER\` for user data

---

## For Development (Linux/Mac in Codespace)

The app works on any OS for CLI testing:

```bash
# From workspace root
python scanner/main.py <file_path> --cli

# Data stored in ~/.CYBERTRACKER/ on Linux/Mac
```

Proper Windows integration (context menu + exe) only works on Windows.

---

## Next Steps

- Build: `python build.py`
- Generate registry: `python generate_context_menu.py`
- Install: Double-click `install_context_menu.reg`
- Test: Right-click any file, select "Scan with CYBERTRACKER"
