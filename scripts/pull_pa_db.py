"""
Pull a backup of the live SQLite database (or JSON dump) from PythonAnywhere
to the local `backups/` directory using the PythonAnywhere Files API.

Usage (PowerShell):
    $env:PA_API_TOKEN = "<your-pythonanywhere-api-token>"
    .\venv_name\Scripts\python.exe scripts\pull_pa_db.py

Optional environment variables:
    PA_USERNAME     (default: eilam20)
    PA_REMOTE_PATH  (e.g. /home/eilam20/my_project/db.sqlite3)
"""
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

PA_USERNAME = os.environ.get("PA_USERNAME", "eilam20")
PA_API_TOKEN = os.environ.get("PA_API_TOKEN")
PA_REMOTE_PATH = os.environ.get("PA_REMOTE_PATH")


def find_remote_db_path(headers):
    """Discover the webapp's source_directory and locate the SQLite DB file."""
    webapps_url = f"https://www.pythonanywhere.com/api/v0/user/{PA_USERNAME}/webapps/"
    res = requests.get(webapps_url, headers=headers, timeout=30)
    if res.status_code != 200 or not res.json():
        print(f"Could not list webapps ({res.status_code}): {res.text}", file=sys.stderr)
        sys.exit(1)

    source_dir = res.json()[0].get("source_directory", "").rstrip("/")
    print(f"Detected PythonAnywhere source directory: {source_dir}")

    dir_url = f"https://www.pythonanywhere.com/api/v0/user/{PA_USERNAME}/files/path{source_dir}/"
    dir_res = requests.get(dir_url, headers=headers, timeout=30)
    if dir_res.status_code != 200:
        print(f"Could not list {source_dir} ({dir_res.status_code}): {dir_res.text}", file=sys.stderr)
        sys.exit(1)

    entries = dir_res.json()
    for candidate in ("db.sqlite3", "ski_db_prod"):
        if candidate in entries:
            return f"{source_dir}/{candidate}"

    for name in entries:
        if name.endswith(".sqlite3") or name.endswith(".db"):
            return f"{source_dir}/{name}"

    print(f"No SQLite file found in {source_dir}. Files present:", file=sys.stderr)
    for name in sorted(entries):
        print(f"  - {name}", file=sys.stderr)
    print("\nNote: If your site already uses MySQL (DEBUG=False), there may be no SQLite file, or you can pass PA_REMOTE_PATH.", file=sys.stderr)
    sys.exit(1)


def main():
    if not PA_API_TOKEN:
        print("Error: PA_API_TOKEN environment variable is not set.", file=sys.stderr)
        print("Get your API token from PythonAnywhere -> Account -> API token.", file=sys.stderr)
        sys.exit(1)

    headers = {"Authorization": f"Token {PA_API_TOKEN}"}
    remote_path = PA_REMOTE_PATH or find_remote_db_path(headers)

    url = f"https://www.pythonanywhere.com/api/v0/user/{PA_USERNAME}/files/path{remote_path}"
    print(f"Downloading {remote_path} from PythonAnywhere...")
    response = requests.get(url, headers=headers, stream=True, timeout=60)
    if response.status_code != 200:
        print(f"Failed ({response.status_code}): {response.text}", file=sys.stderr)
        sys.exit(1)

    backup_dir = Path(__file__).resolve().parent.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = Path(remote_path).name
    dest = backup_dir / f"{filename}.{timestamp}.bak"

    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=65536):
            if chunk:
                f.write(chunk)

    size_kb = dest.stat().st_size / 1024
    print(f"Saved backup to: {dest} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
