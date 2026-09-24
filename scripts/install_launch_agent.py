#!/usr/bin/env python3
"""Install the per-user Friday launchd schedule for this checkout."""

import os
import pathlib
import plistlib
import subprocess


LABEL = "com.hanhan-mom.weekly-paper-tracker"
ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = pathlib.Path.home() / "Library/LaunchAgents" / f"{LABEL}.plist"
LOG = pathlib.Path.home() / "Library/Logs/weekly-paper-tracker.log"


def main():
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if TARGET.exists():
        raise FileExistsError(f"Already installed: {TARGET}")
    job = {
        "Label": LABEL,
        "ProgramArguments": ["/bin/sh", str(ROOT / "scripts/run-weekly.sh")],
        "StartCalendarInterval": {"Weekday": 5, "Hour": 11, "Minute": 0},
        "StandardOutPath": str(LOG),
        "StandardErrorPath": str(LOG),
    }
    with TARGET.open("wb") as output:
        plistlib.dump(job, output)
    try:
        subprocess.run(
            ["launchctl", "bootstrap", f"gui/{os.getuid()}", str(TARGET)],
            check=True,
        )
    except subprocess.CalledProcessError:
        TARGET.unlink()
        raise
    print(f"Installed {LABEL} at {TARGET}")


if __name__ == "__main__":
    main()
