#!/usr/bin/env python3
"""Deliver a researcher-owned TeamViewer callback without printing its credential."""

import argparse
from pathlib import Path
import shlex
import subprocess


COMPONENT = (
    "com.teamviewer.teamviewer.market.mobile/"
    "com.teamviewer.remotecontrolviewlib.activity.WebLoginActivity"
)
PREFIX = "tvoneweblogin://centralizedclientlogin?"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("callback_file", type=Path, help="Private file from a fresh owned login")
    parser.add_argument("--serial", help="ADB serial of the signed-out test device")
    parser.add_argument("--user", type=int, help="Disposable Android user ID")
    parser.add_argument("--root", action="store_true", help="Use su for cross-user lab delivery")
    args = parser.parse_args()

    callback = args.callback_file.read_text(encoding="utf-8").strip()
    if not callback.startswith(PREFIX) or any(c in callback for c in "\r\n\x00"):
        parser.error("callback_file is not one TeamViewer centralized login URI")

    command = "am start"
    if args.user is not None:
        command += f" --user {args.user}"
    command += (
        " -a android.intent.action.VIEW"
        f" -d {shlex.quote(callback)}"
        f" -n {COMPONENT}"
    )
    if args.root:
        command = f"su -c {shlex.quote(command)}"

    adb = ["adb"]
    if args.serial:
        adb += ["-s", args.serial]
    result = subprocess.run(adb + ["shell", command], capture_output=True, text=True, check=False)
    if result.returncode != 0 or "Error:" in result.stdout or "SecurityException" in result.stdout:
        raise SystemExit("Callback intent was not delivered; check the target install and user state")
    print("Callback intent delivered; verify the account state in TeamViewer")


if __name__ == "__main__":
    main()
