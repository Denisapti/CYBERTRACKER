# main.py - Application Entry Point

## Overview

`main.py` is the primary entry point for the CyberTracker scanner. It orchestrates the file scanning workflow by computing a file's SHA-256 hash and checking it against the threat intelligence database.

## Purpose

Acts as the user-facing CLI application that:
1. Accepts file paths from command line
2. Computes cryptographic hashes
3. Queries threat intelligence database
4. Returns structured JSON verdict

## File Location
```
scanner/main.py
```

## Usage

### Basic Syntax
```bash
python scanner/main.py <file_path>
```

### Examples

**Scan a suspicious executable:**
```bash
python scanner/main.py /home/user/Downloads/unknown_app.exe
```

**Scan a system binary:**
```bash
python scanner/main.py /usr/bin/curl
```

**Scan a potential malware:**
```bash
python scanner/main.py ./malicious_script.sh
```

## Function Reference

### main(file_path)

Orchestrates the scanning workflow.

**Parameters:**
- `file_path` (str): Absolute or relative path to file to scan

**Process:**
1. Computes SHA-256 hash using `hashing.sha256_file()`
2. Queries database using `db.check_hash()`
3. Builds JSON verdict

**Output:**
- If hash found: Returns verdict with malware details
- If hash not found: Returns verdict with clean status

**Example:**
```python
main("/path/to/file")
```

## Code Structure

```python
import sys
import json
from hashing import sha256_file
from db import check_hash

def main(file_path):
    # 1. Compute file hash
    file_hash = sha256_file(file_path)
    
    # 2. Query database
    result = check_hash(file_hash)
    
    # 3. Build verdict
    if result:
        malware_name, malware_family = result
        verdict = {
            "file_hash": file_hash,
            "known_malware": True,
            "malware_name": malware_name,
            "malware_family": malware_family,
            "detection_method": "Threat intelligence hash match"
        }
    else:
        verdict = {
            "file_hash": file_hash,
            "known_malware": False,
            "detection_method": "No match in threat intelligence database"
        }
    
    # 4. Output JSON
    print(json.dumps(verdict, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)
    
    main(sys.argv[1])
```

## Imports

| Import | Source | Purpose |
|--------|--------|---------|
| `sys` | Python stdlib | Command-line argument handling |
| `json` | Python stdlib | JSON serialization |
| `sha256_file` | hashing.py | File hashing |
| `check_hash` | db.py | Database lookup |

## Return Values

### Verdict Structure (Known Malware)

```json
{
  "file_hash": "a1b2c3d4e5f6...",
  "known_malware": true,
  "malware_name": "Trojan.Generic",
  "malware_family": "PE/Trojan",
  "detection_method": "Threat intelligence hash match"
}
```

### Verdict Structure (Unknown File)

```json
{
  "file_hash": "9z8y7x6w5v4u...",
  "known_malware": false,
  "detection_method": "No match in threat intelligence database"
}
```

## Error Handling

### Argument Validation
- **Requirement**: Exactly one argument (file path)
- **Error**: Prints usage message and exits with code 1
- **Example**:
  ```bash
  $ python main.py
  Usage: python main.py <file_path>
  ```

### File Access Errors
- **Handling**: Propagated from `hashing.sha256_file()`
- **Behavior**: Python exception if file not found/unreadable

### Database Errors
- **Handling**: Propagated from `db.check_hash()`
- **Behavior**: Python exception if database unavailable

## Integration Points

### Upstream
- **CLI User** - Provides file path as argument

### Downstream
- **hashing.sha256_file()** - Computes hash (see [hashing.py](module-hashing.md))
- **db.check_hash()** - Queries database (see [db.py](module-db.md))

## Output Formats

### To STDOUT
- **Format**: JSON with 2-space indentation
- **Content**: Verdict object with detection results
- **Usage**: Can be piped to other tools or redirected to file

### Exit Codes
- **0**: Success (regardless of match/no-match)
- **1**: Invalid arguments
- **Exception**: Unhandled errors (file not found, etc.)

## Data Flow

```
User Input: /path/to/file
    ↓
main() receives file_path
    ↓
sha256_file(file_path)
    ↓
Check hash in database
    ↓
Build JSON verdict
    ↓
print(json.dumps(verdict))
    ↓
Output to stdout
```

## Related Documentation

- **[Architecture Overview](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module reference
- **[hashing.py](module-hashing.md)** - Hash computation
- **[db.py](module-db.md)** - Database operations
- **[Setup & Usage](SETUP_AND_USAGE.md)** - Build and run instructions

---

## Quick Links

- **[README](README.md)** - Project overview
- **[Architecture](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module index

---

Back to: [README](README.md) | [All Modules](MODULES.md)
