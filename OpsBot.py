
import os
import re
from datetime import datetime

# ── CONFIGURATION 
INPUT_LOG_FILE  = "server.log"
OUTPUT_ALERT_FILE = "security_alerts.txt"

# Keywords OpsBot watches for (case-insensitive match)
ALERT_KEYWORDS = ["CRITICAL", "ERROR", "FAILED LOGIN"]

# ── STEP 1 : FILE PARSING 
def read_log_file(filepath):
    """Read the log file line by line and return all lines."""
    if not os.path.exists(filepath):
        print(f"[OpsBot ERROR] Log file '{filepath}' not found.")
        return []

    with open(filepath, "r") as f:
        lines = f.readlines()

    print(f"[OpsBot] Loaded '{filepath}' — {len(lines)} total lines found.")
    return lines


# ── STEP 2 : PATTERN MATCHING
def filter_alert_lines(lines):
    """
    Scan each line for CRITICAL, ERROR, or FAILED LOGIN.
    Returns only the lines that match any alert keyword.
    """
    alert_lines = []

    for line in lines:
        # re.search is case-insensitive; check all keywords
        if any(re.search(keyword, line, re.IGNORECASE) for keyword in ALERT_KEYWORDS):
            alert_lines.append(line.strip())

    print(f"[OpsBot] Pattern matching complete — {len(alert_lines)} alert lines detected "
          f"out of {len(lines)} total lines.")
    return alert_lines


# ── STEP 3 : DATA STRUCTURING
def count_error_types(alert_lines):
    """
    Count frequency of each alert type using a dictionary.
    Example output: { "ERROR": 5, "CRITICAL": 2, "FAILED LOGIN": 3 }
    """
    frequency = {keyword: 0 for keyword in ALERT_KEYWORDS}

    for line in alert_lines:
        for keyword in ALERT_KEYWORDS:
            if re.search(keyword, line, re.IGNORECASE):
                frequency[keyword] += 1

    return frequency


# ── STEP 4 : REPORT GENERATION
def write_alert_report(alert_lines, frequency, output_path):
    """Write filtered critical lines + summary into security_alerts.txt."""

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

   with open(output_path, "w", encoding="utf-8") as f:

        # ── Header ──────────────────────────────────────────
        f.write("=" * 62 + "\n")
        f.write("        OpsBot — SECURITY ALERT REPORT\n")
        f.write("=" * 62 + "\n")
        f.write(f"  Generated : {generated_at}\n")
        f.write(f"  Source    : {INPUT_LOG_FILE}\n")
        f.write(f"  Total Alerts Found : {len(alert_lines)}\n")
        f.write("=" * 62 + "\n\n")

        # ── Error Frequency Summary ──────────────────────────
        f.write("[ ALERT FREQUENCY SUMMARY ]\n")
        f.write("-" * 35 + "\n")
        for keyword, count in frequency.items():
            bar = "█" * count          # simple ASCII bar chart
            f.write(f"  {keyword:<15} : {count:>3}  {bar}\n")
        f.write("-" * 35 + "\n\n")

        # ── Filtered Alert Lines ─────────────────────────────
        f.write("[ DETAILED ALERT LINES ]\n")
        f.write("-" * 62 + "\n")
        for i, line in enumerate(alert_lines, start=1):
            f.write(f"  [{i:02d}] {line}\n")
        f.write("\n" + "=" * 62 + "\n")
        f.write("  END OF REPORT — Reviewed by OpsBot\n")
        f.write("=" * 62 + "\n")

    print(f"[OpsBot] Report written to '{output_path}' successfully.")


# ── STEP 5 : AUTOMATION — FILE SIZE CONFIRMATION ──────────────
def confirm_output_file(output_path):
    """Use os module to confirm the alert file was created & print its size."""
    if os.path.exists(output_path):
        size_bytes = os.path.getsize(output_path)
        size_kb    = size_bytes / 1024
        print(f"[OpsBot] Confirmation — '{output_path}' created successfully.")
        print(f"         File size : {size_bytes} bytes ({size_kb:.2f} KB)")
    else:
        print(f"[OpsBot ERROR] Output file '{output_path}' was NOT created.")


# ── MAIN ORCHESTRATOR ─────────────────────────────────────────
def run_opsbot():
    print("\n" + "=" * 62)
    print("         OpsBot — Log Automation Engine STARTED")
    print("=" * 62 + "\n")

    # Step 1 — Parse
    all_lines = read_log_file(INPUT_LOG_FILE)
    if not all_lines:
        return

    # Step 2 — Filter
    alert_lines = filter_alert_lines(all_lines)

    # Step 3 — Count frequencies
    frequency = count_error_types(alert_lines)
    print("[OpsBot] Error frequency count:")
    for k, v in frequency.items():
        print(f"         {k} → {v}")

    # Step 4 — Generate report
    write_alert_report(alert_lines, frequency, OUTPUT_ALERT_FILE)

    # Step 5 — Confirm via os module
    confirm_output_file(OUTPUT_ALERT_FILE)

    print("\n[OpsBot] All tasks complete. Check 'security_alerts.txt' for your report.")
    print("=" * 62 + "\n")


# ── ENTRY POINT ───────────────────────────────────────────────
if __name__ == "__main__":
    run_opsbot()
