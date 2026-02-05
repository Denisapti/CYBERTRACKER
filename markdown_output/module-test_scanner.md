# test_scanner.py - Testing Utilities

## Overview

`test_scanner.py` is a verification script that validates the scanner's functionality by testing hash lookup against a known malware hash from the database.

## Purpose

Responsible for:
1. Retrieving test data from database
2. Verifying hash lookup functionality
3. Confirming threat detection works
4. Providing feedback on scanner health

## File Location
```
scanner/test_scanner.py
```

## Usage

### Running the Script
```bash
python scanner/test_scanner.py
```

### Expected Output (Success)

If database contains malware signatures:
```
Testing with known malware hash: abc123def456...
Expected: Trojan.Generic (PE/Executable)

✓ FOUND: Trojan.Generic (PE/Executable)
```

### Expected Output (No Data)

If database is empty:
```
No hashes found in database!
```

### When to Run
- **After setup**: Verify import succeeded
- **Before first scan**: Confirm system operational
- **After updates**: Validate dataload
- **Troubleshooting**: Test database connectivity

## Code Structure

```python
#!/usr/bin/env python3
import sqlite3
from db import check_hash

# Get a known malware hash from the database
conn = sqlite3.connect("malware_hashes.db")
c = conn.cursor()
c.execute("SELECT sha256, malware_name, malware_family FROM malware_hashes LIMIT 1")
result = c.fetchone()
conn.close()

if result:
    known_hash, malware_name, malware_family = result
    print(f"Testing with known malware hash: {known_hash}")
    print(f"Expected: {malware_name} ({malware_family})\n")
    
    # Test the lookup
    result = check_hash(known_hash)
    if result:
        found_name, found_family = result
        print(f"✓ FOUND: {found_name} ({found_family})")
    else:
        print("✗ NOT FOUND (unexpected!)")
else:
    print("No hashes found in database!")
```

## Imports

| Import | Source | Purpose |
|--------|--------|---------|
| `sqlite3` | Python stdlib | Database access |
| `check_hash` | db.py | Lookup, verify function |

## Test Flow

### Phase 1: Retrieve Test Data
```python
conn = sqlite3.connect("malware_hashes.db")
c = conn.cursor()
c.execute("SELECT sha256, malware_name, malware_family FROM malware_hashes LIMIT 1")
result = c.fetchone()
conn.close()
```

**Purpose**: Get any malware record from database  
**Result**: `(hash, name, family)` tuple or None  

### Phase 2: Pass Known Hash
```python
result = check_hash(known_hash)
```

**Input**: SHA-256 hash from database  
**Expected**: Should find the hash we just retrieved  
**Result**: `(name, family)` tuple or None  

### Phase 3: Validate Result

**Success Case**:
```python
if result:
    found_name, found_family = result
    print(f"✓ FOUND: {found_name} ({found_family})")
```

**Failure Case**:
```python
else:
    print("✗ NOT FOUND (unexpected!)")
```

## Data Flow

```
Start Test
    ↓
Connect to database
    ↓
Retrieve first malware record
    ↓
Has records?
    ├─ YES:
    │   ├─ Display test hash
    │   ├─ Display expected values
    │   ├─ Call check_hash(test_hash)
    │   ├─ Hash found?
    │   │   ├─ YES: Print ✓ FOUND
    │   │   └─ NO: Print ✗ NOT FOUND
    │   └─ End
    └─ NO:
        └─ Print "No hashes found in database!"
```

## Integration Points

### Upstream
- **Developer/CI process** - Manual execution
- **Test suite** (future) - Automated testing

### Downstream
- **db.py** - Uses check_hash() function
- **malware_hashes.db** - Reads test data
- **Output** - Console output for verification

## Validation Checks

### Database State
- ✓ Database file exists and is accessible
- ✓ malware_hashes table exists
- ✓ Table contains data records

### Lookup Function
- ✓ `check_hash()` executes without error
- ✓ Returns correct result type
- ✓ Matches expected data

### Data Integrity
- ✓ Retrieved hash matches returned hash
- ✓ Malware name/family are consistent
- ✓ No data corruption detected

## Setup Verification

### Complete Verification Sequence

```bash
# Step 1: Initialize database
python scanner/init_db.py
# Output: Database initialized.

# Step 2: Import threat intelligence
python scanner/import_hashes.py
# Output: Import complete.

# Step 3: Test system (THIS SCRIPT)
python scanner/test_scanner.py
# Output: ✓ FOUND: [malware name]

# Step 4: Ready for production
python scanner/main.py /path/to/file
```

## Interpreting Results

### ✓ FOUND Result
```
Testing with known malware hash: abc123...
Expected: Trojan.Generic (PE/Trojan)

✓ FOUND: Trojan.Generic (PE/Trojan)
```

**Meaning**: System operational and ready  
**Next Step**: Begin scanning files

### ✗ NOT FOUND Result
```
Testing with known malware hash: abc123...
Expected: Trojan.Generic (PE/Trojan)

✗ NOT FOUND (unexpected!)
```

**Meaning**: Hash lookup failed unexpectedly  
**Cause**: Possible data corruption or bug  
**Action**: Check [Troubleshooting](#troubleshooting) section

### No Hashes Found
```
No hashes found in database!
```

**Meaning**: Database exists but is empty  
**Cause**: Skipped import step  
**Action**: Run `python import_hashes.py`

## Output Symbols

| Symbol | Meaning | Context |
|--------|---------|---------|
| ✓ | Success | Hash found in database |
| ✗ | Failure | Hash not found (unexpected) |
| (blank) | Info | Hash being tested |

## Exit Behavior

This script doesn't explicitly set exit codes, but:
- **Normal completion**: Exit code 0
- **Unhandled exception**: Exit code 1 + error message

## Advanced Usage

### Extended Testing

Create a more comprehensive test:
```python
# Check multiple known hashes
conn = sqlite3.connect("malware_hashes.db")
c = conn.cursor()
c.execute("SELECT sha256, malware_name FROM malware_hashes LIMIT 5")
results = c.fetchall()
conn.close()

passed = 0
for hash_val, expected_name in results:
    result = check_hash(hash_val)
    if result:
        passed += 1

print(f"Passed {passed}/{len(results)} tests")
```

### Performance Testing

Measure lookup speed:
```python
import time

conn = sqlite3.connect("malware_hashes.db")
c = conn.cursor()
c.execute("SELECT sha256 FROM malware_hashes LIMIT 100")
hashes = [row[0] for row in c.fetchall()]
conn.close()

start = time.time()
for h in hashes:
    check_hash(h)
elapsed = time.time() - start

print(f"100 lookups in {elapsed:.3f} seconds")
print(f"Average: {elapsed/100*1000:.2f} ms per lookup")
```

## Related Documentation

- **[Architecture Overview](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module reference
- **[db.py](module-db.md)** - Database operations
- **[Setup & Usage](SETUP_AND_USAGE.md)** - Complete setup guide

## Troubleshooting

### "No hashes found in database!"

**Cause**: CSV not imported  
**Solution**:
```bash
python scanner/import_hashes.py
python scanner/test_scanner.py
```

### "✗ NOT FOUND (unexpected!)"

**Cause**: Possible database corruption  
**Solution**:
```bash
# Delete and recreate database
rm scanner/malware_hashes.db
python scanner/init_db.py
python scanner/import_hashes.py
python scanner/test_scanner.py
```

### Database Connection Error

**Cause**: Database locked or corrupted  
**Solution**:
```bash
# Check database
sqlite3 scanner/malware_hashes.db "SELECT COUNT(*) FROM malware_hashes"

# Verify schema
sqlite3 scanner/malware_hashes.db ".schema"
```

### Import Appears Incomplete

**Cause**: Large CSV taking time to process  
**Solution**:
```bash
# Count records
sqlite3 scanner/malware_hashes.db "SELECT COUNT(*) FROM malware_hashes"

# Verify import progress
python scanner/test_scanner.py
```

---

## Quick Links

- **[README](README.md)** - Project overview
- **[Architecture](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module index
- **[Setup & Usage](SETUP_AND_USAGE.md)** - Installation guide

---

Back to: [README](README.md) | [All Modules](MODULES.md)
