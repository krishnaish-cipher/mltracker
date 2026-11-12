import json
import sys
import hashlib
import csv
import shutil
from pathlib import Path
from datetime import datetime, timezone


def init_repo():
    tracker_dir = Path(".mltracker")
    snapshots_dir = tracker_dir / "snapshots"
    history_file = tracker_dir / "history.json"

    snapshots_dir.mkdir(parents=True, exist_ok=True)

    if not history_file.exists():
        history_file.write_text("[]\n", encoding="utf-8")

    print("Initialized empty ML Tracker repository in .mltracker/")


def hash_generator(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def get_csv_metrics(file_path):
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

        if len(rows) == 0:
            return 0, 0

        num_rows = len(rows)
        num_cols = len(rows[0])

    return num_rows, num_cols


def commit_file(file_path, message=""):
    path = Path(file_path)

    tracker_dir = Path(".mltracker")
    history_file = tracker_dir / "history.json"
    snapshots_dir = tracker_dir / "snapshots"

    if not tracker_dir.exists():
        print("Error: Not an ML Tracker repository. Please run init first.")
        return

    if not path.exists():
        print(f"Error: File '{file_path}' not found.")
        return

    if not path.is_file():
        print(f"Error: '{file_path}' is not a file.")
        return

    try:
        file_hash = hash_generator(path)
        rows, cols = get_csv_metrics(path)
    except (OSError, UnicodeError, csv.Error) as e:
        print(f"Error reading CSV file: {e}")
        return

    if history_file.exists():
        history = json.loads(history_file.read_text(encoding="utf-8"))
    else:
        history = []

    # Check the latest commit for this particular file
    latest_commit = next(
        (commit for commit in reversed(history)
         if commit.get("file") == str(path)
         or commit.get("file") == path.name),
        None
    )

    if latest_commit and latest_commit["hash"] == file_hash:
        print("No changes detected. This file is identical to the last commit.")
        print(f"Hash: {file_hash}")
        return

    snapshots_dir.mkdir(parents=True, exist_ok=True)

    snapshot_path = snapshots_dir / f"{file_hash}.csv"

    if not snapshot_path.exists():
        shutil.copy2(path, snapshot_path)
        print(f"Snapshot stored: {snapshot_path}")
    else:
        print("Snapshot already exists (same content)")

    commit_record = {
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(),
        "hash": file_hash,
        "file": str(path),
        "rows": rows,
        "columns": cols,
        "message": message
    }

    history.append(commit_record)

    history_file.write_text(
        json.dumps(history, indent=2),
        encoding="utf-8"
    )

    print(f"Hash: {file_hash}")
    print(f"Rows: {rows}")
    print(f"Columns: {cols}")

    if message:
        print(f"Message: {message}")

    print("Committed successfully!")


def show_log():
    tracker_dir = Path(".mltracker")
    history_file = tracker_dir / "history.json"

    if not tracker_dir.exists():
        print("Error: Not an ML Tracker repository. Please initialize first.")
        return

    if not history_file.exists():
        print("No history found.")
        return

    history = json.loads(history_file.read_text(encoding="utf-8"))

    if len(history) == 0:
        print("No commits yet.")
        return

    print("=" * 60)
    print(f"ML Tracker History (Total commits: {len(history)})")
    print("=" * 60)

    for commit in reversed(history):
        short_hash = commit["hash"][:12]

        print(f"Timestamp : {commit['timestamp']}")
        print(f"Hash      : {short_hash}")
        print(f"File      : {commit['file']}")
        print(f"Rows      : {commit['rows']}")
        print(f"Columns   : {commit['columns']}")

        if commit.get("message"):
            print(f"Message   : {commit['message']}")
        else:
            print("Message   : No message")

        print("-" * 60)


def status_file(file_path):
    path = Path(file_path)

    tracker_dir = Path(".mltracker")
    history_file = tracker_dir / "history.json"

    if not tracker_dir.exists():
        print("Error: Not an ML Tracker repository. Please initialize first.")
        return

    if not path.exists():
        print(f"Error: File '{file_path}' not found.")
        return

    if not path.is_file():
        print(f"Error: '{file_path}' is not a file.")
        return

    try:
        current_hash = hash_generator(path)
        rows, cols = get_csv_metrics(path)
    except (OSError, UnicodeError, csv.Error) as e:
        print(f"Error reading CSV file: {e}")
        return

    print(f"File     : {path.name}")
    print(f"Hash     : {current_hash[:12]}...")
    print(f"Rows     : {rows}")
    print(f"Columns  : {cols}")
    print("-" * 40)

    if not history_file.exists():
        print("Status   : No commits yet. This is an untracked file.")
        return

    history = json.loads(history_file.read_text(encoding="utf-8"))

    file_commits = [
        commit for commit in history
        if commit.get("file") == str(path)
        or commit.get("file") == path.name
    ]

    if not file_commits:
        print("Status   : No commits yet. This is an untracked file.")
        return

    last_commit = file_commits[-1]

    if last_commit["hash"] == current_hash:
        print("Status   : Up to date (same as last commit)")
        print(f"Last commit message: {last_commit.get('message', 'No message')}")
    else:
        print("Status   : Modified (different from last commit)")
        print(f"Last committed hash : {last_commit['hash'][:12]}...")
        print(f"Last committed rows : {last_commit['rows']}")
        print(f"Last committed cols : {last_commit['columns']}")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python main.py <command>")
        print("Available commands: init, commit, log, status")

    else:
        command = sys.argv[1]

        if command == "init":
            init_repo()

        elif command == "commit":

            if len(sys.argv) < 3:
                print("Usage: python main.py commit <file.csv> [-m \"message\"]")

            else:
                file_path = sys.argv[2]
                message = ""

                if "-m" in sys.argv:
                    m_index = sys.argv.index("-m")

                    if m_index + 1 < len(sys.argv):
                        message = " ".join(sys.argv[m_index + 1:])
                    else:
                        print("Error: Please provide a message after -m")
                        sys.exit(1)

                commit_file(file_path, message)

        elif command == "log":
            show_log()

        elif command == "status":

            if len(sys.argv) < 3:
                print("Usage: python main.py status <file.csv>")

            else:
                status_file(sys.argv[2])

        else:
            print(f"Unknown command: {command}")
