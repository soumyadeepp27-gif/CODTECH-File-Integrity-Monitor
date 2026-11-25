"""
monitor.py
Core logic for the File Integrity Monitor (FIM).
Calculates SHA-256 cryptographic hashes for files in a target directory,
saves them to a baseline JSON file, and detects unauthorized modifications,
additions, or deletions.
"""

import hashlib
import json
import os


def calculate_sha256(file_path: str) -> str:
    """
    Reads a file in 4KB chunks and returns its SHA-256 hexadecimal hash.
    Reading in chunks prevents high memory usage on large files.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def scan_directory(folder_path: str) -> dict:
    """
    Walks through the target directory and maps each file's relative path
    to its SHA-256 hash.
    """
    file_hashes = {}
    for root, _, files in os.walk(folder_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, folder_path)
            file_hashes[rel_path] = calculate_sha256(full_path)
    return file_hashes


def create_baseline(folder_path: str, baseline_file: str = "baseline.json") -> dict:
    """
    Scans the target folder and saves the current file hashes as the trusted baseline.
    """
    if not os.path.isdir(folder_path):
        return {"error": f"Folder not found: '{folder_path}'"}

    hashes = scan_directory(folder_path)
    with open(baseline_file, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=4)

    return {
        "status": "success",
        "files_indexed": len(hashes),
        "baseline_file": baseline_file,
        "hashes": hashes
    }


def check_integrity(folder_path: str, baseline_file: str = "baseline.json") -> dict:
    """
    Compares the current state of the target folder against the saved baseline.
    Identifies modified, newly added, and deleted files.
    """
    if not os.path.isdir(folder_path):
        return {"error": f"Folder not found: '{folder_path}'"}

    if not os.path.isfile(baseline_file):
        return {"error": "No baseline found! Please create a baseline first (Option 1)."}

    with open(baseline_file, "r", encoding="utf-8") as f:
        baseline_hashes = json.load(f)

    current_hashes = scan_directory(folder_path)

    modified = []
    added = []
    deleted = []
    unchanged = []

    # Check for modified or unchanged files, and newly added files
    for rel_path, current_hash in current_hashes.items():
        if rel_path not in baseline_hashes:
            added.append(rel_path)
        elif baseline_hashes[rel_path] != current_hash:
            modified.append(rel_path)
        else:
            unchanged.append(rel_path)

    # Check for deleted files
    for rel_path in baseline_hashes:
        if rel_path not in current_hashes:
            deleted.append(rel_path)

    return {
        "modified": modified,
        "added": added,
        "deleted": deleted,
        "unchanged": unchanged
    }