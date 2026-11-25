# File Integrity Monitor (FIM)

## Internship Details
- **INTERN ID:** CITS9043
- **FULL NAME:** Soumyadeep Sarkar
- **NO. OF WEEKS:** 12 Weeks
- **PROJECT NAME:** File Integrity Monitor
- **PROJECT SCOPE:** Develop a lightweight Python cybersecurity utility that generates SHA-256 cryptographic baselines for critical directories and detects unauthorized file modifications, additions, or deletions.

---

## Features
- **SHA-256 Hashing:** Generates unique 256-bit cryptographic fingerprints for every file in a target directory.
- **JSON Baseline Storage:** Saves trusted file hashes locally in `baseline.json`.
- **Tamper Detection:** Instantly flags modified, newly added, and deleted files.
- **Zero External Dependencies:** Built entirely with Python's standard library (`hashlib`, `os`, `json`).

## Folder Structure
```text
CODTECH-File-Integrity-Monitor/
├── src/
│   ├── monitor.py
│   └── main.py
├── test_folder/
│   ├── config.txt
│   └── notes.txt
├── docs/
│   └── DOCUMENTATION.md
├── screenshots/
│   ├── baseline_output.png
│   └── tamper_detected.png
└── README.md