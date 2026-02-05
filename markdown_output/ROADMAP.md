# Roadmap & Next Steps

Future improvements and planned features for the CyberTracker malware detection system. Based on analysis of the development plan documented in [nextStep.txt](nextStep.txt).

## Overview

CyberTracker currently provides basic malware detection via hash matching. This roadmap outlines planned enhancements to improve automation, scalability, and functionality.

## Phase 1: Automation (High Priority)

The primary goal is to automate the CSV update and ingestion process to keep threat intelligence data current.

### 1.1 Track Last Update Timestamp

**Goal**: Know when data was last synchronized with MalwareBazaar

**Implementation**:
Create metadata tracking file:
```
scanner/metadata/last_update.json
```

**Metadata File Structure**:
```json
{
  "last_sync_timestamp": "2024-02-05T14:30:00Z",
  "csv_checksum": "a1b2c3d4e5f6...",
  "record_count": 1234567,
  "data_source": "MalwareBazaar",
  "data_version": "2024-02-05"
}
```

**Fields**:
- `last_sync_timestamp`: ISO 8601 timestamp of last sync
- `csv_checksum`: SHA-256 of downloaded CSV for change detection
- `record_count`: Number of hashes in database
- `data_source`: Source identifier
- `data_version`: Dataset version/date

**Benefits**:
- Avoid redundant downloads
- Track data freshness
- Enable incremental updates
- Provide audit trail

### 1.2 Check MalwareBazaar for Updates

**Goal**: Automatically detect when new threat intelligence is available

**Implementation Options**:

#### Option A: API Query (Preferred)
**MalwareBazaar API Endpoint**:
```
https://api.abuse.ch/api/v1/
```

**Query Purpose**:
- Get `last-modified` timestamp of dataset
- Compare with stored `last_sync_timestamp`
- Determine if download needed

**Pseudocode**:
```python
def check_for_updates():
    # Get remote last-modified timestamp
    remote_timestamp = query_malware_bazaar_api()
    
    # Load local metadata
    local_timestamp = load_metadata()['last_sync_timestamp']
    
    # Compare
    if remote_timestamp > local_timestamp:
        return True  # Update available
    else:
        return False  # Data current
```

#### Option B: CSV Checksum Comparison
**Fallback Method** (if API unavailable):
- Download CSV header/sample
- Compute checksum
- Compare with stored checksum
- Download full CSV if different

**Advantage**: Works without API access  
**Disadvantage**: Less efficient, requires download to check

### 1.3 Download Fresh CSV

**Goal**: Automatically fetch latest MalwareBazaar export

**Implementation**:
```python
import requests

def download_csv():
    url = "https://bazaar.abuse.ch/export/csv_hashes.zip"  # or appropriate endpoint
    
    response = requests.get(url, timeout=300)
    
    if response.status_code == 200:
        # Save to data/ directory
        with open('scanner/data/hashes.csv', 'wb') as f:
            f.write(response.content)
        
        # Compute and store checksum
        save_checksum(compute_checksum(response.content))
        return True
    else:
        return False  # Download failed
```

**Features**:
- HTTP(S) connection with timeout
- File versioning option
- Error handling for network failure
- Checksum verification

### 1.4 Update Database

**Goal**: Incorporate new threat data with minimal downtime

**Implementation Approaches**:

#### Approach A: Full Replacement (Current)
```python
# 1. Drop old database
# 2. Recreate schema
# 3. Import fresh CSV
# 4. Update metadata
```

**Pros**: Clean slate, no orphaned records  
**Cons**: Downtime during update, data loss if something fails

#### Approach B: Incremental Addition (Recommended)
```python
# 1. Load existing records into memory (hashes only)
# 2. Process CSV
# 3. For each record:
#    If hash not in existing set:
#      Add to database
#    Else:
#      Skip (already have)
# 4. Update metadata
```

**Pros**: No downtime, fast updates, preserves history  
**Cons**: Database grows over time, more memory usage

#### Approach C: Backup & Swap (Safest)
```python
# 1. Keep current database as backup
# 2. Create new database
# 3. Import fresh CSV into new database
# 4. If all successful:
#    Swap new database as current
#    Archive old database
# 5. If any error:
#    Keep old database active
#    Log error for review
```

**Pros**: Safest, rollback capability, no data loss  
**Cons**: Requires extra disk space temporarily

**Recommendation**: Start with Approach C for safety

### 1.5 Create update_hashes.py Script

**Goal**: Orchestrate entire update process

**Implementation**:
```python
#!/usr/bin/env python3
"""
Automatic malware database update script.
Downloads latest threat intelligence from MalwareBazaar.
Can be run manually or via cron job.
"""

import os
import json
import hashlib
import requests
from datetime import datetime
from import_hashes import load_csv_into_database
from db import get_connection

def load_metadata():
    """Load last update metadata"""
    meta_path = 'scanner/metadata/last_update.json'
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            return json.load(f)
    return None

def save_metadata(metadata):
    """Save update metadata"""
    os.makedirs('scanner/metadata', exist_ok=True)
    with open('scanner/metadata/last_update.json', 'w') as f:
        json.dump(metadata, f, indent=2)

def check_for_updates():
    """Check MalwareBazaar API for new data"""
    # Implementation here
    pass

def download_csv():
    """Download latest CSV from MalwareBazaar"""
    # Implementation here
    pass

def backup_database():
    """Backup current database before update"""
    # Implementation here
    pass

def update_database():
    """Load CSV into database (incremental approach)"""
    # Implementation here
    pass

def main():
    print("Checking for MalwareBazaar updates...")
    
    # Check if update needed
    if not check_for_updates():
        print("Data is current. No update needed.")
        return
    
    print("Update available. Downloading...")
    
    # Download CSV
    if not download_csv():
        print("ERROR: Download failed")
        return
    
    # Backup current database
    backup_database()
    
    # Update database
    try:
        update_database()
        print("Update successful!")
    except Exception as e:
        print(f"ERROR: Update failed: {e}")
        print("Using backup database...")
        # Restore from backup

if __name__ == "__main__":
    main()
```

## Phase 2: Integration & Automation (Medium Priority)

### 2.1 Cron Job Scheduling

**Goal**: Automatically check for updates on schedule

**Implementation**:
```bash
# Edit crontab
crontab -e

# Add weekly update job
0 2 * * 0 cd /path/to/scanner && python update_hashes.py
```

**Options**:
- Daily: `0 2 * * *` (2 AM daily)
- Weekly: `0 2 * * 0` (2 AM Sundays)
- Monthly: `0 2 1 * *` (2 AM first day)

### 2.2 Error Handling & Logging

Comprehensive error handling:
```python
import logging

logging.basicConfig(
    filename='scanner/logs/update.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    # update logic
except requests.ConnectTimeout:
    logging.error("Network timeout")
except IOError as e:
    logging.error(f"File I/O error: {e}")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
```

## Phase 3: Enhanced Functionality (Lower Priority)

### 3.1 Multi-Source Support

Support multiple threat intelligence sources:
- VirusTotal API
- APT Notes
- YARA rules
- Custom hash lists

**Implementation**: Pluggable source adapters

### 3.2 Incremental Hashing

Hash computation for very large files:
- Stream-based processing
- Progress indicators
- Timeout handling

### 3.3 Bulk Scanning

Scan directories recursively:
```bash
python scanner/main.py --directory /path/to/scan --recursive
```

**Features**:
- Directory traversal
- File filtering
- Progress reporting
- Batch result output

### 3.4 Webhook Integration

Post results to external systems:
```python
def post_result_webhook(verdict):
    """Send scan result to webhook endpoint"""
    requests.post(
        os.getenv('WEBHOOK_URL'),
        json=verdict,
        timeout=10
    )
```

### 3.5 Web API

REST API for scanning:
```
POST /api/scan
Content-Type: application/json

{
    "file_path": "/path/to/file"
}

Response:
{
    "file_hash": "...",
    "known_malware": true,
    ...
}
```

## Phase 4: Advanced Features (Future)

### 4.1 Machine Learning Classification
- Pattern recognition
- Behavior analysis
- Anomaly detection

### 4.2 Threat Correlation
- Identify malware variants
- Track campaigns
- Link related samples

### 4.3 Reporting & Analytics
- Historical trend analysis
- Detection reports
- Executive summaries

### 4.4 Integration with SIEM
- Splunk connector
- ELK stack integration
- Syslog output

## Implementation Priority

### Immediate (Next Sprint)
1. ✅ Metadata tracking
2. ✅ Check for updates logic
3. ✅ CSV download functionality
4. ✅ update_hashes.py script
5. ✅ Error handling

### Short-term (1-2 months)
1. Cron job setup
2. Logging infrastructure
3. Testing framework
4. Documentation updates
5. Incremental update approach

### Medium-term (2-3 months)
1. CLI improvements
2. Bulk scanning
3. Multi-source support
4. Basic web interface
5. Performance optimization

### Long-term (3+ months)
1. REST API
2. Machine learning
3. Advanced analytics
4. SIEM integration
5. Database scalability

## Testing Strategy

### Unit Tests
- Test each function independently
- Validate error handling
- Mock external APIs

### Integration Tests
- Test full update workflow
- Verify database operations
- Check file I/O

### Regression Tests
- Ensure existing functionality preserved
- Validate backward compatibility

## Documentation Updates

These roadmap features will require documentation of:
- New modules and functions
- Configuration options
- API endpoints
- Troubleshooting guides
- Examples and use cases

## Success Metrics

Track progress with:
- ✅ Test coverage (target: >80%)
- ✅ Update frequency (target: automatic weekly)
- ✅ Detection accuracy (track false positives)
- ✅ Performance metrics (hash lookup <10ms)
- ✅ User adoption

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| API downtime | No updates | Fallback to manual download |
| Large CSV | Memory issues | Streaming processing |
| Data corruption | Invalid detections | Backup & verify procedures |
| Network failures | Incomplete update | Retry logic + notifications |

## Questions for Product Team

1. What's the priority order for Phase 2-4 features?
2. Should we support multiple malware data sources initially?
3. Is real-time detection (<10ms) a requirement?
4. What's the maximum database size we need to support?
5. Do we need historical data retention?

## Related Documentation

- **[Architecture Overview](ARCHITECTURE.md)** - Current system design
- **[Data Sources](DATA_SOURCES.md)** - MalwareBazaar integration
- **[Setup & Usage](SETUP_AND_USAGE.md)** - Current capabilities

---

## Feedback

Have suggestions for this roadmap? Please create an issue in the repository.

---

Back to: [README](README.md)
