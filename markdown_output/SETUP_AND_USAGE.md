# Setup & Usage Guide

Complete guide to installing, configuring, and using the CyberTracker malware detection system.

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **OS**: Linux, macOS, or Windows
- **Disk Space**: Minimum 500 MB (depends on CSV size)
- **Memory**: 512 MB minimum

### Check Python Version
```bash
python --version
# Should output: Python 3.8.x or higher
```

## Installation

### Step 1: Obtain Code

Clone or download the CyberTracker repository:
```bash
git clone <repository-url>
cd CYBERTRACKER
```

Or if already in workspace:
```bash
cd <workspace>/CYBERTRACKER
```

### Step 2: Verify Structure

Confirm the project structure:
```bash
ls -la scanner/
```

Expected output:
```
main.py
db.py
hashing.py
init_db.py
import_hashes.py
test_scanner.py
data/
  hashes.csv
```

### Step 3: Check Python Installation

Verify required modules available:
```bash
python -c "import sqlite3, hashlib; print('OK')"
# Output: OK (all modules present)
```

## Configuration

### Database Location
**Current Setting**: Relative to working directory
```python
# In scanner/db.py
DB_PATH = "malware_hashes.db"
```

**To Change**:
Edit `scanner/db.py` and change `DB_PATH` to absolute path:
```python
DB_PATH = "/path/to/malware_hashes.db"
```

### CSV Source
**Current Setting**: Located in `scanner/data/`
```python
# In scanner/import_hashes.py
CSV_PATH = os.path.join(BASE_DIR, "data", "hashes.csv")
```

**Note**: CSV file must be in UTF-8 format with comment lines starting with `#`

## Initialization

### Step 1: Create Database Schema

Initialize the SQLite database:
```bash
cd scanner
python init_db.py
```

**Expected Output**:
```
Database initialized.
```

**What It Does**:
- Creates `malware_hashes.db` file
- Defines table schema with columns for hashes and metadata
- Prepares database for data import

**Verification**:
```bash
ls -la malware_hashes.db
sqlite3 malware_hashes.db ".tables"
# Should output: malware_hashes
```

### Step 2: Import Threat Intelligence Data

Load malware signatures from CSV:
```bash
python import_hashes.py
```

**Expected Output**:
```
Import complete.
```

**What It Does**:
- Reads `data/hashes.csv`
- Parses threat intelligence records
- Inserts hashes into database
- Removes duplicate entries automatically

**Verification**:
```bash
sqlite3 malware_hashes.db "SELECT COUNT(*) FROM malware_hashes"
# Should output: [number of records]

sqlite3 malware_hashes.db "SELECT * FROM malware_hashes LIMIT 1"
# Should show: hash | name | family | source
```

### Step 3: Test Installation

Verify system is operational:
```bash
python test_scanner.py
```

**Expected Output** (with data imported):
```
Testing with known malware hash: abc123def456...
Expected: Trojan.Generic (PE/Executable)

✓ FOUND: Trojan.Generic (PE/Executable)
```

**Expected Output** (without data):
```
No hashes found in database!
```

If you see `No hashes found`, ensure import completed successfully.

## Usage

### Basic File Scanning

Scan a single file:
```bash
python main.py /path/to/file
```

### Example Scans

**Scan a downloaded file**:
```bash
python scanner/main.py ~/Downloads/unknown_app.exe
```

**Scan a system binary**:
```bash
python scanner/main.py /usr/bin/curl
```

**Scan with output saved**:
```bash
python scanner/main.py ~/file.zip > /tmp/scan_result.json
```

### Output Format

The scanner returns structured JSON:

**Known Malware Example**:
```json
{
  "file_hash": "abc123def456e7f8...",
  "known_malware": true,
  "malware_name": "Trojan.Generic",
  "malware_family": "PE/Trojan",
  "detection_method": "Threat intelligence hash match"
}
```

**Clean File Example**:
```json
{
  "file_hash": "9z8y7x6w5v4u3t2s...",
  "known_malware": false,
  "detection_method": "No match in threat intelligence database"
}
```

### Interpreting Results

| Field | Meaning | Values |
|-------|---------|--------|
| `file_hash` | SHA-256 of file | 64-character hex string |
| `known_malware` | Threat detected | `true` or `false` |
| `malware_name` | Signature | e.g., "Trojan.Generic" |
| `malware_family` | Classification | e.g., "PE/Executable" |
| `detection_method` | How it was found | Hash match or unknown |

## Common Workflows

### Scan Downloads Directory

Check all downloaded files:
```bash
for file in ~/Downloads/*; do
    echo "Scanning: $file"
    python scanner/main.py "$file" | grep known_malware
done
```

### Scan and Save Results

Scan with structured output:
```bash
python scanner/main.py /path/to/file | tee scan_log.json
```

### Batch Scanning

Create a script `batch_scan.sh`:
```bash
#!/bin/bash
SCAN_DIR=$1
for file in "$SCAN_DIR"/*; do
    if [ -f "$file" ]; then
        echo "=== Scanning: $file ==="
        python scanner/main.py "$file"
        echo ""
    fi
done
```

Usage:
```bash
chmod +x batch_scan.sh
./batch_scan.sh ~/Downloads
```

## Data Updates

### Updating Threat Intelligence

When new MalwareBazaar CSV available:

```bash
# Step 1: Backup old database (optional)
cp scanner/malware_hashes.db scanner/malware_hashes.db.backup

# Step 2: Replace CSV file
# (Copy new hashes.csv to scanner/data/)

# Step 3: Re-initialize and import
python scanner/init_db.py
python scanner/import_hashes.py

# Step 4: Verify update
python scanner/test_scanner.py
```

### Incremental Update Strategy

To keep old data while adding new:

1. Use tool [future feature] for incremental import
2. Or manually merge databases

See: [Roadmap](ROADMAP.md) for planned features

## Troubleshooting

### Database Issues

**Problem**: "no such table: malware_hashes"  
**Solution**: Run `python init_db.py` first

**Problem**: "database is locked"  
**Solution**: Wait a moment and retry, or close other connections

### Import Issues

**Problem**: "No such file or directory: hashes.csv"  
**Solution**: Ensure CSV is in `scanner/data/hashes.csv`

**Problem**: "Error inserting row"  
**Solution**: Check CSV format - should be UTF-8 with proper headers

### Scanning Issues

**Problem**: "No such file or directory" when scanning  
**Solution**: Use absolute path or check file exists

**Problem**: JSON output has errors  
**Solution**: Verify database imported successfully with `test_scanner.py`

### Performance Issues

**Problem**: Scanning is slow  
**Solution**: 
- Large files are expected to take time
- Check disk I/O with `iostat`
- Ensure database not being accessed by other process

## Advanced Configuration

### Custom Database Location

Edit `scanner/db.py`:
```python
import os

# Use environment variable or fixed path
DB_PATH = os.getenv('CYBERTRACKER_DB', '/opt/cybertracker/malware_hashes.db')
```

### Custom CSV Location

Edit `scanner/import_hashes.py`:
```python
# Use environment variable or different path
CSV_PATH = os.getenv('CYBERTRACKER_CSV', '/opt/data/malware_hashes.csv')
```

### Environment Variables

Create `.env` or set manually:
```bash
export CYBERTRACKER_DB=/opt/cybertracker/malware_hashes.db
export CYBERTRACKER_CSV=/opt/data/hashes.csv
```

## Integration Examples

### Python Script Integration

```python
import sys
sys.path.insert(0, '/path/to/scanner')
from hashing import sha256_file
from db import check_hash

file_path = "/path/to/scan"
hash_val = sha256_file(file_path)
result = check_hash(hash_val)

if result:
    print(f"MALWARE DETECTED: {result[0]}")
else:
    print("File is clean")
```

### JSON Processing

```bash
# Scan and extract just the verdict
python scanner/main.py /path/to/file | jq '.known_malware'

# Extract malware name if detected
python scanner/main.py /path/to/file | jq 'if .known_malware then .malware_name else "Clean" end'
```

### Webhook Integration (Future)

See: [Roadmap](ROADMAP.md) for planned webhook support

## Performance Tuning

### Database Optimization

Rebuild index after large import:
```bash
sqlite3 scanner/malware_hashes.db "REINDEX"
```

Analyze query performance:
```bash
sqlite3 scanner/malware_hashes.db "ANALYZE"
```

### Hash Computation

Chunk size (in `hashing.py`):
```python
chunk_size = 8192  # bytes - reduce for slow I/O, increase for SSD
```

## Related Documentation

- **[Architecture Overview](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module reference
- **[Roadmap & Next Steps](ROADMAP.md)** - Future improvements

---

## Quick Start (TL;DR)

```bash
cd scanner

# Initialize
python init_db.py

# Import data
python import_hashes.py

# Test
python test_scanner.py

# Scan files
python main.py /path/to/file
```

---

Back to: [README](README.md)
