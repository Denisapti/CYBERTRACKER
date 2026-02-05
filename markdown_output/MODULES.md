# Module Reference

Complete overview of all Python modules in CyberTracker. Each module handles a specific responsibility in the system.

## Module Map

| Module | Purpose | Key Functions | Used By |
|--------|---------|----------------|---------|
| [main.py](module-main.md) | Application entry point | `main(file_path)` | Command line |
| [db.py](module-db.md) | Database operations | `get_connection()`, `check_hash()` | main.py |
| [hashing.py](module-hashing.md) | File hashing | `sha256_file(path)` | main.py |
| [init_db.py](module-init_db.md) | Database initialization | Schema creation | Setup phase |
| [import_hashes.py](module-import_hashes.md) | Data import | CSV to DB loading | Setup phase |
| [test_scanner.py](module-test_scanner.md) | Testing | Verify functionality | Development |

## Quick Reference

### Entry Point Module

#### [main.py](module-main.md) - Application Entry Point
```python
python scanner/main.py <file_path>
```
- Accepts file path from command line
- Computes hash and checks database
- Returns JSON verdict
- Handles argument validation
- **See**: [Detailed Documentation](module-main.md)

### Core Utility Modules

#### [hashing.py](module-hashing.md) - SHA-256 Hashing
```python
from hashing import sha256_file
file_hash = sha256_file("/path/to/file")
```
- Computes SHA-256 hash of files
- Memory-efficient chunked reading
- Returns hex digest string
- **See**: [Detailed Documentation](module-hashing.md)

#### [db.py](module-db.md) - Database Layer
```python
from db import check_hash, get_connection
result = check_hash(sha256_hash)
```
- Manages SQLite connections
- Queries malware hash table
- Returns malware metadata or None
- **See**: [Detailed Documentation](module-db.md)

### Setup & Initialization Modules

#### [init_db.py](module-init_db.md) - Database Initialization
```bash
python scanner/init_db.py
```
- Creates database schema
- Initializes malware_hashes table
- Idempotent (safe to run multiple times)
- **See**: [Detailed Documentation](module-init_db.md)

#### [import_hashes.py](module-import_hashes.md) - Data Import
```bash
python scanner/import_hashes.py
```
- Loads threat intelligence CSV
- Parses and cleans data
- Inserts records into database
- Handles duplicates gracefully
- **See**: [Detailed Documentation](module-import_hashes.md)

### Testing Modules

#### [test_scanner.py](module-test_scanner.md) - Functionality Testing
```bash
python scanner/test_scanner.py
```
- Verifies scanner operation
- Uses known malware hash
- Tests database lookup
- Validates threat detection
- **See**: [Detailed Documentation](module-test_scanner.md)

## Module Dependencies

### Dependency Graph
```
main.py (Entry Point)
├── hashing.py (Hash computation)
└── db.py (Database access)

init_db.py (Standalone)
└── sqlite3 (standard library)

import_hashes.py (Standalone)
├── csv (standard library)
├── sqlite3 (standard library)
└── os (standard library)

test_scanner.py (Standalone)
├── sqlite3 (standard library)
└── db.py (Database access)
```

### Import Relationships
- **main.py** imports: `sys`, `json`, `hashing`, `db`
- **db.py** imports: `sqlite3`
- **hashing.py** imports: `hashlib`
- **init_db.py** imports: `sqlite3`
- **import_hashes.py** imports: `csv`, `sqlite3`, `os`
- **test_scanner.py** imports: `sqlite3`, `db`

## Execution Modes

### Normal Usage
```bash
# Scan a file
python scanner/main.py /path/to/suspicious_file
```
Uses: main.py → hashing.py → db.py

### First-Time Setup
```bash
# Step 1: Initialize database
python scanner/init_db.py

# Step 2: Import threat data
python scanner/import_hashes.py
```
Uses: init_db.py, import_hashes.py

### Verification
```bash
# Run tests
python scanner/test_scanner.py
```
Uses: test_scanner.py → db.py

## File Organization

```
scanner/
├── main.py                    # Application entry point
├── db.py                      # Database module
├── hashing.py                 # Hashing module
├── init_db.py                 # Initialization script
├── import_hashes.py           # Data import script
├── test_scanner.py            # Test script
├── __pycache__/               # Compiled Python files
├── malware_hashes.db          # SQLite database
└── data/
    └── hashes.csv             # Threat intelligence data
```

## Configuration Points

### Database Path
**File**: `db.py`
```python
DB_PATH = "malware_hashes.db"
```

### CSV Path
**File**: `import_hashes.py`
```python
CSV_PATH = os.path.join(BASE_DIR, "data", "hashes.csv")
```

### Hash Chunk Size
**File**: `hashing.py`
```python
chunk_size = 8192  # 8KB blocks
```

## Related Documentation

- **[Architecture Overview](ARCHITECTURE.md)** - System design and data flow
- **[Setup & Usage](SETUP_AND_USAGE.md)** - How to install and run
- **[Data Sources](DATA_SOURCES.md)** - Threat intelligence information

---

### Module Details

- **[main.py - Application Entry Point](module-main.md)**
- **[db.py - Database Layer](module-db.md)**
- **[hashing.py - File Hashing](module-hashing.md)**
- **[init_db.py - Database Initialization](module-init_db.md)**
- **[import_hashes.py - Data Import](module-import_hashes.md)**
- **[test_scanner.py - Testing Utilities](module-test_scanner.md)**

---

Back to: [README](README.md)
