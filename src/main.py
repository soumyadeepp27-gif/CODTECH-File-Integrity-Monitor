"""
main.py
Command-Line Interface (CLI) for the File Integrity Monitor (FIM).
Allows users to create a SHA-256 baseline and scan for file tampering.
"""

from monitor import create_baseline, check_integrity


def print_integrity_report(report: dict) -> None:
    """Formats and displays the integrity check results."""
    if "error" in report:
        print(f"\n[ERROR] {report['error']}\n")
        return

    print("\n" + "=" * 50)
    print("           FILE INTEGRITY REPORT")
    print("=" * 50)

    tampered = bool(report["modified"] or report["added"] or report["deleted"])

    if not tampered:
        print("  [SAFE] All files are intact. No tampering detected.")
    else:
        print("  [ALERT] Unauthorized changes detected!")

    if report["modified"]:
        print("\n  [MODIFIED FILES]:")
        for f in report["modified"]:
            print(f"    ! {f}")

    if report["added"]:
        print("\n  [NEWLY ADDED FILES]:")
        for f in report["added"]:
            print(f"    + {f}")

    if report["deleted"]:
        print("\n  [DELETED FILES]:")
        for f in report["deleted"]:
            print(f"    - {f}")

    print(f"\n  Unchanged files: {len(report['unchanged'])}")
    print("=" * 50 + "\n")


def main() -> None:
    """Main interactive menu loop."""
    print("=== File Integrity Monitor (SHA-256) ===")
    target_folder = input("Enter folder to monitor (press Enter for 'test_folder'): ").strip()
    if not target_folder:
        target_folder = "test_folder"

    while True:
        print(f"\nTarget Folder: {target_folder}")
        print("1. Create / Update Baseline")
        print("2. Check File Integrity")
        print("3. Exit")

        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            result = create_baseline(target_folder)
            if "error" in result:
                print(f"\n[ERROR] {result['error']}\n")
            else:
                print("\n" + "=" * 50)
                print(f"  Baseline created successfully in '{result['baseline_file']}'!")
                print(f"  Total files indexed: {result['files_indexed']}")
                print("=" * 50)
                for path, h in result["hashes"].items():
                    print(f"  {path} -> {h[:16]}...")
                print()

        elif choice == "2":
            report = check_integrity(target_folder)
            print_integrity_report(report)

        elif choice == "3":
            print("Exiting File Integrity Monitor. Stay secure!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()