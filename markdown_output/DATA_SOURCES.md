# Data Sources

Information about threat intelligence sources and data formats used by CyberTracker.

## MalwareBazaar

Primary source of malware threat intelligence for CyberTracker.

### Overview

**MalwareBazaar** is a reputable threat intelligence platform run by abuse.ch that collects malware samples and threat data from security researchers and threat analysts worldwide.

**Website**: https://bazaar.abuse.ch  
**API**: https://api.abuse.ch/api/v1/  
**License**: Varies by dataset

### Data Provided

MalwareBazaar provides:
- **SHA-256 hashes** of known malware samples
- **Malware classifications** and signatures
- **File type information** and characteristics
- **Reporter/researcher** metadata
- **Detection timestamps**

### CSV Export Format

The dataset is exported as a CSV file with the following structure:

#### Header Line
```
# "sha256_hash","signature","file_type_guess","reporter"
```

**Format Notes**:
- Starts with `#` to indicate comment/header
- Contains quoted field names
- Includes commas and special characters

#### Data Records
```
abc123def456...,Trojan.Generic,PE/Executable,security_researcher
def456ghi789...,Worm.Win32,PE/DLL,threat_analyst
```

**Format Notes**:
- No quotes around values (usually)
- Comma-separated fields
- One record per line

### Field Definitions

| CSV Field | Description | Example | Database Field |
|-----------|-------------|---------|-----------------|
| `sha256_hash` | SHA-256 hash of malware | `a1b2c3d4e5f6...` | `sha256` |
| `signature` | Malware name/signature | `Trojan.Generic` | `malware_name` |
| `file_type_guess` | File type/classification | `PE/Executable` | `malware_family` |
| `reporter` | Data source or researcher | `MalwareBazaar` | `source` |

### Data Quality

**Accuracy**:
- Hashes are verified SHA-256 values
- Signatures from multiple security vendors
- Crowdsourced from threat community

**Completeness**:
- Not all malware in the wild
- Focus on publicly available samples
- Regularly updated

**Coverage**:
- Includes known malware families
- Windows, Linux, macOS, mobile platforms
- Various malware types (trojans, worms, ransomware, etc.)

### Update Frequency

- **Data Additions**: Multiple times per week
- **New Samples**: Thousands per week
- **Recommended Refresh**: Weekly or monthly

See: [Roadmap](ROADMAP.md) for planned automatic updates

### Access Methods

#### Direct Download
1. Visit https://bazaar.abuse.ch
2. Download malware hashes CSV
3. Place in `scanner/data/hashes.csv`

#### API Access (Future)
See: [Roadmap](ROADMAP.md) for planned API integration

```python
# Future implementation
import requests

api_url = "https://api.abuse.ch/api/v1/"
response = requests.get(api_url)
```

### Attribution and Citation

When using MalwareBazaar data in reports:

> Data sourced from MalwareBazaar (https://bazaar.abuse.ch), a threat intelligence platform maintained by abuse.ch.

## Local Data Storage

### Storage Location
```
scanner/data/hashes.csv
```

**Note**: CSV file is not version controlled (may be large)

### CSV Processing in CyberTracker

The [import_hashes.py](module-import_hashes.md) script handles:

1. **Comment stripping**: Removes pure comment lines starting with `#`
2. **Header detection**: Identifies header line with quoted field names
3. **CSV parsing**: Uses Python csv.DictReader
4. **Field mapping**: Maps CSV columns to database schema
5. **Data normalization**: Lowercases hashes, trims whitespace
6. **Duplicate handling**: INSERT OR IGNORE prevents duplicates

### Data Validation

#### Hash Validation
```bash
# Check hash format (should be 64 hex characters)
sqlite3 scanner/malware_hashes.db \
  "SELECT LENGTH(sha256) FROM malware_hashes LIMIT 1"
# Output: 64
```

#### Record Counts
```bash
# Count total records
sqlite3 scanner/malware_hashes.db \
  "SELECT COUNT(*) FROM malware_hashes"

# Check for nulls in important fields
sqlite3 scanner/malware_hashes.db \
  "SELECT COUNT(*) FROM malware_hashes WHERE sha256 IS NULL"
# Output: 0 (no nulls expected)
```

#### Data Sample
```bash
sqlite3 scanner/malware_hashes.db \
  ".mode column" \
  "SELECT sha256, malware_name, malware_family FROM malware_hashes LIMIT 5"
```

## Data Privacy & Ethics

### Usage Considerations

**Permission**:
- MalwareBazaar data is publicly available
- Use follows terms of service

**Attribution**:
- Include attribution in reports
- Cite abuse.ch as source

**Responsible Use**:
- Use only for security purposes
- Don't share raw hashes without permission
- Report security issues responsibly

### Limitations

- Hashes don't identify live malware
- Hash-based detection can be evaded by modification
- Database represents known malware, not all threats
- False positives/negatives possible

## Alternative Data Sources

### Other Threat Intelligence Platforms

**VirusTotal**:
- API-based access
- Larger hash database
- Requires API key
- Commercial licensing

**APT Notes & Public IOCs**:
- https://github.com/aptnotes/data
- Community-contributed
- Varies in quality

**YARA Rules**:
- Pattern-based detection
- More complex than hash matching
- Covers malware families

### Integration (Future)

See: [Roadmap](ROADMAP.md) for planned multi-source support

## Database Schema Alignment

### Mapping Process

When importing MalwareBazaar CSV:

```
CSV Column           →  Database Field
sha256_hash          →  sha256
signature            →  malware_name
file_type_guess      →  malware_family
reporter             →  source
```

### Field Transformations

| Transformation | Purpose | Example |
|---|---|---|
| `.strip().lower()` | Hash normalization | `ABC123...` → `abc123...` |
| `.get(..., "Unknown")` | Default values | Missing signature → "Unknown" |
| Quote removal | Header parsing | `"field"` → `field` |

## Data Update Strategy

### Current Approach
- Manual CSV replacement
- Full database re-initialization
- Requires admin action

### Recommended Approach
- Weekly automated updates
- Incremental data loading
- Preserve historical data

See: [Roadmap](ROADMAP.md) for implementation details

## Compliance & Legal

### Terms of Service
- Follow MalwareBazaar ToS
- Respect data source agreements
- Maintain proper attribution

### Data Retention
- Database maintains historical hashes
- No automatic purging
- Administrator controls retention

## Troubleshooting Data Issues

### Wrong Hash Format
**Problem**: Hashes not 64 characters  
**Check**: `SELECT LENGTH(sha256) FROM malware_hashes`  
**Fix**: Re-import with clean CSV

### Missing or Corrupted CSV
**Problem**: Import fails or no data loaded  
**Check**: File exists with valid content  
**Fix**: Download fresh CSV from MalwareBazaar

### Data Quality Issues
**Problem**: Malformed records in import  
**Check**: Review import error messages  
**Fix**: Clean CSV file before import

## Related Documentation

- **[Architecture Overview](ARCHITECTURE.md)** - System design
- **[import_hashes.py](module-import_hashes.md)** - Data loading
- **[Setup & Usage](SETUP_AND_USAGE.md)** - Configuration
- **[Roadmap](ROADMAP.md)** - Future data source plans

---

## Quick Links

- **[README](README.md)** - Project overview
- **[All Modules](MODULES.md)** - Module reference

---

Back to: [README](README.md)
