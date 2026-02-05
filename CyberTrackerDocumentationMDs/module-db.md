# db.py - Database Layer

## Overview

`db.py` provides the database abstraction layer for accessing threat intelligence data. It manages SQLite connections and queries malware hash signatures.

## Purpose

Responsible for:
1. Managing database connections
2. Querying malware signatures
3. Returning threat intelligence metadata
4. Handling database access errors

## File Location
```
scanner/db.py
```

## Configuration

### Database Path
```python
DB_PATH = "malware_hashes.db"
```
- **Location**: Current working directory
- **Type**: SQLite database file
- **Created by**: [init_db.py](module-init_db.md)
- **Populated by**: [import_hashes.py](module-import_hashes.md)

## Function Reference

### get_connection()

Establishes and returns a SQLite database connection.

**Parameters:**
- None

**Returns:**
- `sqlite3.Connection` - Database connection object

**Example:**
```python
from db import get_connection
conn = get_connection()
cursor = conn.cursor()
# ... query ...
conn.close()
```

**Details:**
- Opens connection to `DB_PATH`
- Returns active connection
- Caller responsible for closing

### check_hash(sha256_hash)

Looks up a SHA-256 hash in the malware database.

**Parameters:**
- `sha256_hash` (str): SHA-256 hash in hexadecimal format

**Returns:**
- `tuple` - `(malware_name, malware_family)` if found
- `None` - If hash not in database

**Example:**
```python
from db import check_hash

result = check_hash("a1b2c3d4e5f6...")
if result:
    name, family = result
    print(f"Found: {name} ({family})")
else:
    print("Hash not found")
```

**Process:**
1. Connect to database
2. Execute SELECT query on `malware_hashes` table
3. Fetch result or None
4. Close connection
5. Return result

## Code Structure

```python
import sqlite3

DB_PATH = "malware_hashes.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def check_hash(sha256_hash):
    conn = get_connection()
    c = conn.cursor()
    
    c.execute(
        "SELECT malware_name, malware_family FROM malware_hashes WHERE sha256 = ?",
        (sha256_hash,)
    )
    result = c.fetchone()
    
    conn.close()
    return result
```

## Imports

| Import | Source | Purpose |
|--------|--------|---------|
| `sqlite3` | Python stdlib | Database management |

## Database Schema

### Table: malware_hashes

```sql
CREATE TABLE IF NOT EXISTS malware_hashes (
    sha256 TEXT PRIMARY KEY,
    malware_name TEXT,
    malware_family TEXT,
    source TEXT
)
```

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `sha256` | TEXT | File hash (unique identifier) |
| `malware_name` | TEXT | Malware signature/name |
| `malware_family` | TEXT | Malware family/type |
| `source` | TEXT | Data source (e.g., MalwareBazaar) |

### Indexes
- **Primary Key**: `sha256` - Enables O(1) lookups

## Query Details

### Hash Lookup Query
```sql
SELECT malware_name, malware_family 
FROM malware_hashes 
WHERE sha256 = ?
```

**Query Type**: SELECT (read-only)  
**Performance**: O(1) via primary key index  
**Safe Execution**: Uses parameterized query to prevent SQL injection  

## Data Flow

```
Input: SHA-256 hash string
    ↓
get_connection()
    ↓
Open SQLite file
    ↓
Execute SELECT query
    ↓
Fetch result (one row or None)
    ↓
Close connection
    ↓
Return (malware_name, malware_family) or None
```

## Integration Points

### Upstream
- **main.py** - Requests hash lookups (see [main.py](module-main.py.md))

### Downstream
- **malware_hashes.db** - Physical database file
- **init_db.py** - Creates table schema (see [init_db.py](module-init_db.md))
- **import_hashes.py** - Populates with data (see [import_hashes.py](module-import_hashes.md))

## Usage Examples

### Basic Hash Lookup
```python
from db import check_hash

hash_value = "abc123def456..."
result = check_hash(hash_value)

if result:
    malware_name, family = result
    print(f"Malware detected: {malware_name}")
else:
    print("File is clean")
```

### Integration with main.py
```python
# From main.py
from db import check_hash

result = check_hash(file_hash)

if result:
    malware_name, malware_family = result
    verdict = {
        "known_malware": True,
        "malware_name": malware_name,
        "malware_family": malware_family
    }
```

## Performance Characteristics

### Query Performance
- **Lookup Type**: Primary key search (indexed)
- **Time Complexity**: O(1) constant time
- **Scalability**: Suitable for millions of records

### Connection Management
- **New connection per query**: Simple but creates overhead
- **Optimization opportunity**: Connection pooling for high volume
- **Current design**: Adequate for typical usage

## Error Handling

### Missing Database
- **Behavior**: `sqlite3.OperationalError` raised
- **Cause**: Database not initialized (run [init_db.py](module-init_db.md))
- **Fix**: Run initialization script

### Missing Table
- **Behavior**: `sqlite3.OperationalError` raised
- **Cause**: Table not created or corrupted
- **Fix**: Reinitialize database

### Database Locked
- **Behavior**: `sqlite3.OperationalError` raised
- **Cause**: Another process accessing database
- **Fix**: Wait for other access to complete

## Security Considerations

### SQL Injection Prevention
- **Method**: Parameterized queries (prepared statements)
- **Example**: `WHERE sha256 = ?` with parameter binding
- **Safety**: All queries use this pattern

### Database Access Control
- **Current**: File-based access (no authentication)
- **Assumption**: Trusted execution environment
- **Recommendation**: Protect DB file permissions

## Related Documentation

- **[Architecture Overview](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module reference
- **[main.py](module-main.py.md)** - Uses check_hash()
- **[init_db.py](module-init_db.md)** - Creates schema
- **[import_hashes.py](module-import_hashes.md)** - Populates data

---

## Quick Links

- **[README](README.md)** - Project overview
- **[Architecture](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module index

---

Back to: [README](README.md) | [All Modules](MODULES.md)
