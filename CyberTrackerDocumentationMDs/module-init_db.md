# init_db.py - Database Initialization

## Overview

`init_db.py` is a setup script that creates the SQLite database schema and initializes the malware_hashes table. Run this once during initial project setup.

## Purpose

Responsible for:
1. Creating SQLite database
2. Defining table structure (schema)
3. Initializing primary keys and columns
4. Preparing database for data import

## File Location
```
scanner/init_db.py
```

## Usage

### Running the Script
```bash
python scanner/init_db.py
```

### Expected Output
```
Database initialized.
```

### When to Run
- **First-time setup**: Before first use of scanner
- **Database corruption**: To recreate clean schema
- **Development**: To reset database for testing

### Idempotency
This script is **idempotent** - safe to run multiple times:
```sql
CREATE TABLE IF NOT EXISTS malware_hashes
```
The `IF NOT EXISTS` clause prevents errors on repeated execution.

## Code Structure

```python
import sqlite3

conn = sqlite3.connect("malware_hashes.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS malware_hashes (
    sha256 TEXT PRIMARY KEY,
    malware_name TEXT,
    malware_family TEXT,
    source TEXT
)
""")

conn.commit()
conn.close()

print("Database initialized.")
# Run once via terminal: python init_db.py
```

## Imports

| Import | Source | Purpose |
|--------|--------|---------|
| `sqlite3` | Python stdlib | Database management |

## Database Schema

### File Output
```
malware_hashes.db
```
- **Location**: Current working directory (scanner/)
- **Type**: SQLite 3 database file
- **Size**: ~1 KB (initially, grows with data)

### Table Definition

#### Table: malware_hashes

```sql
CREATE TABLE IF NOT EXISTS malware_hashes (
    sha256 TEXT PRIMARY KEY,
    malware_name TEXT,
    malware_family TEXT,
    source TEXT
)
```

### Column Specifications

| Column | Type | Constraint | Purpose |
|--------|------|-----------|---------|
| `sha256` | TEXT | PRIMARY KEY | Unique file hash identifier |
| `malware_name` | TEXT | None | Human-readable malware name |
| `malware_family` | TEXT | None | Malware classification/family |
| `source` | TEXT | None | Threat intel source reference |

### Primary Key
```sql
sha256 TEXT PRIMARY KEY
```
- **Purpose**: Ensures unique hash entries
- **Index**: Automatic B-tree index
- **Performance**: O(1) lookup time
- **Constraint**: No duplicate hashes allowed

### Data Types

**TEXT columns**
- Store variable-length strings
- No size limit specified
- Suitable for hashes and metadata

**No constraints**
- Allows NULL values in non-key columns
- Flexible for incomplete records

## Execution Flow

### Step-by-Step

```
1. Import sqlite3
2. Create/connect to malware_hashes.db
3. Get cursor for database operations
4. Execute CREATE TABLE IF NOT EXISTS
5. Commit transaction
6. Close connection
7. Print success message
```

### Database File Creation

```
First run:
    └─ malware_hashes.db doesn't exist
    └─ sqlite3.connect() creates empty database
    └─ CREATE TABLE initializes schema
    └─ Database ready for data import

Subsequent runs:
    └─ malware_hashes.db already exists
    └─ sqlite3.connect() opens existing database
    └─ CREATE TABLE IF NOT EXISTS does nothing
    └─ No harm from re-running
```

## Data Flow

```
Execute init_db.py
    ↓
Create connection to database
    ↓
Execute CREATE TABLE statement
    ↓
Commit changes
    ↓
Close connection
    ↓
Database ready for import
```

## Integration Points

### Upstream
- **Administrator/Setup process** - Manual execution
- **CI/CD pipeline** (future) - Automated setup

### Downstream
- **malware_hashes.db** - Created/initialized database file
- **import_hashes.py** - Populates created table (see [import_hashes.py](module-import_hashes.md))
- **db.py** - Queries the initialized table (see [db.py](module-db.md))

## Setup Sequence

### Complete First-Time Setup

```bash
# Step 1: Initialize database schema
python scanner/init_db.py
# Output: Database initialized.

# Step 2: Import threat intelligence data
python scanner/import_hashes.py
# Output: Import complete.

# Step 3: Test the scanner
python scanner/test_scanner.py
# Output: ✓ FOUND: [malware found in test]

# Step 4: Ready for production use
python scanner/main.py /path/to/scan
```

See: [Setup & Usage Guide](SETUP_AND_USAGE.md)

## Database Validation

### Check Database Created
```bash
ls -la scanner/malware_hashes.db
# Should show file size > 0
```

### Check Table Exists
```bash
sqlite3 scanner/malware_hashes.db ".tables"
# Should output: malware_hashes
```

### Check Schema
```bash
sqlite3 scanner/malware_hashes.db ".schema malware_hashes"
# Should show table definition
```

## Modification and Expansion

### Adding Columns
To add new columns later:

```python
c.execute("ALTER TABLE malware_hashes ADD COLUMN date_added TEXT DEFAULT CURRENT_TIMESTAMP")
```

### Removing Columns
```python
# SQLite doesn't support DROP COLUMN easily
# Would require: create new table, copy data, drop old, rename
```

### Changing Constraints
```python
# Requires table recreation in SQLite
```

## Performance Characteristics

### Initial Setup
- **Execution time**: <100 ms
- **Disk usage**: ~1 KB empty database
- **I/O operations**: Minimal (single write)

### Repeated Execution
- **Detection**: Checks if table exists
- **Time**: <10 ms (no operation needed)
- **Safety**: IF NOT EXISTS prevents errors

## Related Documentation

- **[Architecture Overview](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module reference
- **[import_hashes.py](module-import_hashes.md)** - Data import
- **[db.py](module-db.md)** - Database usage
- **[Setup & Usage](SETUP_AND_USAGE.md)** - Complete setup guide

## Troubleshooting

### Database Won't Create
**Problem**: Script runs but no database file appears  
**Check**: Current working directory
```bash
pwd  # Verify in scanner/ directory
python init_db.py
ls -la malware_hashes.db  # Check for file
```

### Permission Denied
**Problem**: Cannot write database  
**Fix**: Check directory permissions
```bash
chmod 755 scanner/
python init_db.py
```

### Database Locked
**Problem**: "database is locked" error  
**Cause**: Another process accessing database
**Fix**: Wait and retry, or close other connections

---

## Quick Links

- **[README](README.md)** - Project overview
- **[Architecture](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module index
- **[Setup & Usage](SETUP_AND_USAGE.md)** - Installation guide

---

Back to: [README](README.md) | [All Modules](MODULES.md)
