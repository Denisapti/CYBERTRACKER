# System Architecture

## Overview

CyberTracker implements a three-layer architecture for malware detection using threat intelligence data.

```
┌─────────────────────────────────────────────────────────┐
│                   INPUT LAYER                           │
│  User provides file path via command line               │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              PROCESSING LAYER                           │
│  • Compute SHA-256 hash of file (hashing.py)            │
│  • Query database for hash match (db.py)                │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              DATA LAYER                                 │
│  SQLite Database (malware_hashes.db)                    │
│  Contains: sha256, malware_name, malware_family, source │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│               OUTPUT LAYER                              │
│  JSON verdict with detection results                    │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. **Initialization Phase**
```
admin: python init_db.py
    ↓
Create SQLite schema
    ↓
Create malware_hashes table
```
*See: [init_db.py](module-init_db.md)*

### 2. **Data Import Phase**
```
admin: python import_hashes.py
    ↓
Read hashes.csv from data/
    ↓
Parse CSV, strip comments
    ↓
Insert into malware_hashes table
    ↓
Database populated with threat intelligence
```
*See: [import_hashes.py](module-import_hashes.md)*

### 3. **Scanning Phase**
```
user: python main.py /path/to/file
    ↓
Compute SHA-256 hash [hashing.py]
    ↓
Query database [db.py]
    ↓
Match found? Yes → Return malware details
             No  → Return clean verdict
    ↓
Output JSON result
```
*See: [main.py](module-main.md)*

### 4. **Testing Phase**
```
dev: python test_scanner.py
    ↓
Fetch known malware hash from DB
    ↓
Run lookup test
    ↓
Verify hash is correctly identified
```
*See: [test_scanner.py](module-test_scanner.py)*

## Component Responsibilities

### Hashing Module (`hashing.py`)
- **Purpose**: Cryptographic file hashing
- **Key Function**: `sha256_file(path)` - Computes SHA-256 of file
- **Design**: Chunked reading (8KB blocks) for memory efficiency
- **Used by**: main.py
- **Details**: [hashing.py Documentation](module-hashing.md)

### Database Module (`db.py`)
- **Purpose**: Threat intelligence data access
- **Key Function**: `check_hash(sha256_hash)` - Lookup hash in database
- **Connection**: SQLite database (malware_hashes.db)
- **Returns**: Tuple of (malware_name, malware_family) or None
- **Used by**: main.py
- **Details**: [db.py Documentation](module-db.md)

### Main Application (`main.py`)
- **Purpose**: Orchestrate scanning workflow
- **Entry Point**: Command-line tool
- **Workflow**: Hash file → Check database → Generate JSON verdict
- **Output Format**: Structured JSON with detection results
- **Details**: [main.py Documentation](module-main.md)

### Initialization (`init_db.py`)
- **Purpose**: One-time database setup
- **Action**: Creates schema and table structure
- **Idempotent**: Uses CREATE TABLE IF NOT EXISTS
- **Run Once**: When setting up new installation
- **Details**: [init_db.py Documentation](module-init_db.md)

### Data Import (`import_hashes.py`)
- **Purpose**: Load threat intelligence data
- **Source**: MalwareBazaar CSV export
- **Process**: Parse, clean, and insert records
- **Handling**: Strips comments, handles encoding, ignores duplicates
- **Details**: [import_hashes.py Documentation](module-import_hashes.md)

### Testing (`test_scanner.py`)
- **Purpose**: Verify scanner functionality
- **Method**: Uses known malware hash from database
- **Validates**: Hash lookup accuracy
- **Output**: Pass/fail indicators
- **Details**: [test_scanner.py Documentation](module-test_scanner.md)

## Database Schema

```sql
CREATE TABLE malware_hashes (
    sha256 TEXT PRIMARY KEY,
    malware_name TEXT,
    malware_family TEXT,
    source TEXT
)
```

### Fields
- **sha256**: SHA-256 hash (primary key, unique identifier)
- **malware_name**: Human-readable malware name/signature
- **malware_family**: Type/family of malware
- **source**: Threat intelligence source (e.g., MalwareBazaar)

## Dependencies

### External Libraries
- **sqlite3** - Database management (Python standard library)
- **hashlib** - Cryptographic hashing (Python standard library)
- **csv** - CSV parsing (Python standard library)
- **os** - File system operations (Python standard library)

### No External Packages Required
All functionality uses Python standard library only.

## Execution Flow

### Normal Usage (File Scanning)
```python
# Command: python main.py /path/to/file

1. Parse command-line argument
2. Call main(file_path)
3. hashing.sha256_file(file_path)
   → Read file in chunks
   → Compute SHA-256
   → Return hex digest
4. db.check_hash(file_hash)
   → Connect to database
   → Query for hash
   → Return result or None
5. Build verdict JSON
6. Print to stdout
```

### First-Time Setup
```python
# Command sequence: 
# python init_db.py
# python import_hashes.py

1. Initialize database
   → Create schema
   → Create table
2. Import threat intelligence
   → Read CSV
   → Parse records
   → Insert into database
   → Database ready for scanning
```

## Performance Considerations

### Hash Computation
- **Chunked reading**: 8KB buffer prevents memory bloat
- **Applicable to**: Large files without loading entire contents

### Database Lookup
- **Primary key index**: O(1) lookup time on sha256
- **Scalable to**: Millions of malware signatures 
- **Dev appended note:**  currently 2.6 Million signatures stored

### CSV Import
- **Streaming parse**: Processes CSV line-by-line
- **Duplicate handling**: INSERT OR IGNORE prevents errors

## Security Considerations

### Hash Integrity
- **Algorithm**: SHA-256 (cryptographically secure)
- **Standard**: NIST approved, widely used in threat intelligence

### Database Access
- **Direct file access**: malware_hashes.db should be protected
- **No authentication required**: Assumes trusted environment

### Data Source
- **MalwareBazaar**: Reputable threat intelligence platform
- **Verification**: Users should verify CSV integrity

## Related Documentation

- **[Setup & Usage](SETUP_AND_USAGE.md)** - How to run the system
- **[All Modules](MODULES.md)** - Module index and overview
- **[Data Sources](DATA_SOURCES.md)** - MalwareBazaar information
- **[Roadmap](ROADMAP.md)** - Planned improvements

---

Back to: [README](README.md)
