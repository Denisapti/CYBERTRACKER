# hashing.py - File Hashing Utilities

## Overview

`hashing.py` provides cryptographic file hashing functionality using the SHA-256 algorithm. It implements memory-efficient chunked file reading for handling large files.

## Purpose

Responsible for:
1. Computing SHA-256 hashes of files
2. Reading files in memory-efficient chunks
3. Returning hash values as hexadecimal strings
4. Supporting files of any size

## File Location
```
scanner/hashing.py
```

## Function Reference

### sha256_file(path)

Computes the SHA-256 hash of a file.

**Parameters:**
- `path` (str): Absolute or relative path to the file

**Returns:**
- `str` - SHA-256 hash as hexadecimal string (64 characters)

**Example:**
```python
from hashing import sha256_file

file_hash = sha256_file("/home/user/document.pdf")
print(file_hash)  # a1b2c3d4e5f6...
```

**Details:**
- Reads file in 8KB chunks to conserve memory
- Memory usage independent of file size
- Returns lowercase hexadecimal hash
- Time complexity: O(n) where n = file size

## Code Structure

```python
import hashlib

def sha256_file(path):
    """Computes the SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
```

## Imports

| Import | Source | Purpose |
|--------|--------|---------|
| `hashlib` | Python stdlib | Cryptographic hashing |

## Algorithm Details

### SHA-256
- **Name**: Secure Hash Algorithm 256-bit
- **Output**: 256-bit (32-byte) hash
- **Format**: 64 hexadecimal characters
- **Standard**: NIST standardized
- **Security**: Cryptographically secure

### Hash Examples

**Example 1: Small file**
```
File: /etc/hostname
Content: ubuntu
SHA-256: ab1234567890... (64 hex chars)
```

**Example 2: Binary executable**
```
File: /usr/bin/curl
Size: ~200 KB
SHA-256: def4567890ab... (64 hex chars)
```

## Implementation Details

### Chunked Reading

**Why Chunked?**
- Memory efficiency for large files (gigabytes)
- Constant memory usage regardless of file size
- Standard pattern for file hashing

**Chunk Size**
```python
chunk_size = 8192  # 8 KB
```
- Balance between memory and I/O efficiency
- Suitable for modern systems

**Process**
```python
h = hashlib.sha256()      # Initialize hasher
with open(path, "rb") as f:
    while chunk := f.read(8192):  # Read 8KB chunks
        h.update(chunk)            # Update hash
return h.hexdigest()       # Get hex string
```

### Walrus Operator
```python
while chunk := f.read(8192):
```
- Python 3.8+ syntax
- Assigns and checks in one expression
- Loops until `f.read(8192)` returns empty bytes (EOF)

## Data Flow

```
Input: file_path
    ↓
Open file in binary mode
    ↓
Initialize SHA-256 hasher
    ↓
Loop:
  └─ Read 8KB chunk
  └─ Update hash
  └─ Repeat until EOF
    ↓
Get hexadecimal hash
    ↓
Return 64-character hash string
```

## Usage Examples

### Basic Usage
```python
from hashing import sha256_file

hash_value = sha256_file("/path/to/file")
print(hash_value)
# Output: a1b2c3d4e5f6g7h8i9j0...
```

### Integration with main.py
```python
# From main.py
from hashing import sha256_file

file_hash = sha256_file(file_path)
# Use hash value for database lookup
```

### Error Handling
```python
from hashing import sha256_file

try:
    file_hash = sha256_file("/nonexistent/file")
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Permission denied")
```

## Performance Characteristics

### Time Complexity
- **O(n)** where n = file size
- Must read entire file for cryptographic hash
- Performance limited by disk I/O

### Space Complexity
- **O(1)** constant memory
- 8KB buffer + hash object only
- Independent of file size
- Suitable for scanning large files

### Benchmark Examples

| File Size | Approximate Time |
|-----------|------------------|
| 1 MB | <1 ms |
| 100 MB | ~50 ms |
| 1 GB | ~500 ms |

*Times vary based on disk speed and system load*

## File Modes

### Binary Mode
```python
with open(path, "rb") as f:
```
- Opens file in binary read mode
- Reads raw bytes without encoding
- Required for accurate hashing
- Works with any file type (text, binary, executable)

## Integration Points

### Upstream
- **main.py** - Calls sha256_file() (see [main.py](module-main.py.md))

### Downstream
- **File system** - Reads physical files
- **hashlib** - Uses SHA-256 implementation

## Error Scenarios

### File Not Found
```python
sha256_file("/nonexistent/path")
# Raises: FileNotFoundError
```

### Permission Denied
```python
sha256_file("/root/private/file")  # Without permission
# Raises: PermissionError
```

### File Deleted During Read
```python
# File deleted between open and read
# Raises: OSError
```

### Directory Instead of File
```python
sha256_file("/home/user/")  # Directory, not file
# Raises: IsADirectoryError
```

## Output Format

### Hexadecimal String
- **Length**: 64 characters
- **Charset**: 0-9, a-f (lowercase)
- **Example**: `a1b2c3d4e5f6789012345678901234567890123456789012345678901234`

### Case Consistency
- Output is lowercase hexadecimal
- Database lookups expect lowercase
- Comparison should be case-insensitive if needed

## Related Documentation

- **[Architecture Overview](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module reference
- **[main.py](module-main.py.md)** - Uses sha256_file()
- **[db.py](module-db.md)** - Uses hash result

---

## Quick Links

- **[README](README.md)** - Project overview
- **[Architecture](ARCHITECTURE.md)** - System design
- **[All Modules](MODULES.md)** - Module index

---

Back to: [README](README.md) | [All Modules](MODULES.md)
