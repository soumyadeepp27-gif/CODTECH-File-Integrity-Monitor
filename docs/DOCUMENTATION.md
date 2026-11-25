# Project Documentation: File Integrity Monitor (FIM)

## 1. Objective
Attackers and malware often alter system configuration files or plant unauthorized scripts to maintain persistence. A **File Integrity Monitor (FIM)** detects these changes immediately by verifying cryptographic hashes against a known-good baseline.

## 2. System Architecture
- **`src/monitor.py` (Core Engine):** Recursively scans directories using `os.walk()`, computes SHA-256 hashes in 4KB chunks via `hashlib`, stores baselines in `baseline.json`, and compares current hashes against the baseline.
- **`src/main.py` (CLI Interface):** Provides a menu-driven interface to create baselines and view formatted integrity alerts.

## 3. Why SHA-256?
SHA-256 exhibits the **avalanche effect**: changing even a single character or space inside a file produces a completely different 64-character hexadecimal hash. This makes it impossible for an attacker to silently alter a file without triggering an alert.

## 4. Test Cases
| Scenario | Action Taken | Expected Result |
| :--- | :--- | :--- |
| Normal State | Run Option 2 right after Option 1 | `[SAFE] All files are intact.` |
| File Tampering | Add a single word to `test_folder/notes.txt` | `[MODIFIED FILES]: ! notes.txt` |
| Unauthorized File | Create `test_folder/malware.txt` | `[NEWLY ADDED FILES]: + malware.txt` |
| File Deletion | Delete `test_folder/config.txt` | `[DELETED FILES]: - config.txt` |