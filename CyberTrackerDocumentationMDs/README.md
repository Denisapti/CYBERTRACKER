# CyberTracker: Malware Detection System

Welcome to CyberTracker, a threat intelligence-powered file scanning system that uses cryptographic hashing to identify known malware.

IF YOU NEED HELP READING THESE FILES USE THE FOLOWING:
**Browser Tools That Render Markdown Locally**

1. **MarkView – Modern Markdown Viewer (Chrome/Chromium extension)**  
    Installs as a browser extension, then you can open `.md` files (local or remote). It renders GitHub-Flavored Markdown nicely, supports diagrams (Mermaid) and math, and you can drag local files into the browser and see them rendered instantly. It doesn’t require a separate service or account — just the extension.
    
2. **Markdown Reader (Browser extension)**  
    A simple browser extension that will render `.md` files in the browser. Great for double-clicking Markdown files and seeing them nicely formatted without any server or hosting setup.
    
3. **Online Markdown Viewers (no install)**  
    Sites like **mdview.io** let you upload or drag-and-drop your `.md` files and instantly render them in the browser. It doesn’t host your repo, but it _does_ interpret your Markdown cleanly without installs — others just need to upload the files.  
    Other similar viewers include generic “Markdown Viewer” sites where you paste or upload `.md` and get rendered HTML.

## Quick Overview

CyberTracker is a Python-based application that:
- Computes SHA-256 hashes of files
- Compares them against a database of known malware signatures
- Returns threat intelligence results in JSON format
- Sources data from MalwareBazaar threat intelligence database

## Navigation

### Getting Started
- **[Setup & Usage Guide](SETUP_AND_USAGE.md)** - Installation, configuration, and running the scanner

### Understanding the System
- **[Architecture Overview](ARCHITECTURE.md)** - System design, data flow, and component relationships
- **[All Modules](MODULES.md)** - Quick reference to all Python modules
- **[Data Sources](DATA_SOURCES.md)** - Information about threat intelligence sources (MalwareBazaar)

### Module Documentation
Core modules with detailed documentation:
- **[db.py](module-db.md)** - Database layer and hash lookups
- **[hashing.py](module-hashing.md)** - File hashing utilities
- **[main.py](module-main.md)** - Main application entry point
- **[init_db.py](module-init_db.md)** - Database initialization
- **[import_hashes.py](module-import_hashes.md)** - CSV data import
- **[test_scanner.py](module-test_scanner.md)** - Testing utilities

### Future & Development
- **[Roadmap & Next Steps](ROADMAP.md)** - Planned improvements and automation goals

## Project Structure

```
scanner/
├── main.py              # Entry point
├── db.py                # Database operations
├── hashing.py           # SHA-256 hashing
├── init_db.py          # DB initialization
├── import_hashes.py    # CSV to DB import
├── test_scanner.py     # Testing utilities
├── malware_hashes.db   # SQLite database
└── data/
    └── hashes.csv      # Threat intelligence data
```

## Quick Start

```bash
# Initialize database
python scanner/init_db.py

# Import malware signatures
python scanner/import_hashes.py

# Scan a file
python scanner/main.py /path/to/suspicious/file
```

## Key Features

✅ **Efficient Hashing** - Chunked file reading for memory efficiency  
✅ **Database Backed** - SQLite for fast lookups  
✅ **Threat Intelligence** - Powered by MalwareBazaar data  
✅ **JSON Output** - Structured results for downstream processing  
✅ **Testable** - Includes test utilities  

## License

[Add your license here]

---

**Need help?** Check the [Setup & Usage Guide](SETUP_AND_USAGE.md) or explore the [Architecture Overview](ARCHITECTURE.md).



git demo change pls ignore