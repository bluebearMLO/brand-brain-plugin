#!/usr/bin/env python3
"""Apply a JSON list of exact text edits (as returned by Brand Brain agents) to files.

Usage:
  python3 apply_edits.py edits.json [--root <project-root>] [--apply]

edits.json is a JSON array (or an object with an "edits" array) of
  {"file": "<path>", "old": "<exact existing text>", "new": "<replacement>", "why": "<one line>"}
Relative paths resolve against --root (default: current directory).

Without --apply it is a dry run: every edit is checked (file exists, "old" found exactly
once, counting earlier edits to the same file) and a report is printed. With --apply, the
files are written only if every edit passes. Nothing is half-applied.
"""
import argparse
import json
import os
import re
import sys


def load(path):
    text = open(path, encoding="utf-8").read()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Agents often wrap JSON in prose or a ```json fence; take the first array.
        m = re.search(r"\[\s*\{.*\}\s*\]", text, re.S)
        if not m:
            sys.exit(f"{path}: no JSON array found")
        data = json.loads(m.group(0))
    if isinstance(data, dict):
        data = data.get("edits", [])
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edits", nargs="+", help="one or more JSON edit files")
    ap.add_argument("--root", default=".")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    edits = []
    for p in a.edits:
        for e in load(p):
            e["_src"] = os.path.basename(p)
            edits.append(e)

    buffers, failures = {}, []
    for i, e in enumerate(edits, 1):
        f, old, new = e.get("file"), e.get("old"), e.get("new")
        tag = f"[{i}] {e['_src']} → {f}"
        if not f or old is None or new is None:
            failures.append(f"{tag}: missing file/old/new")
            continue
        path = f if os.path.isabs(f) else os.path.join(a.root, f)
        if path not in buffers:
            if not os.path.exists(path):
                failures.append(f"{tag}: file not found ({path})")
                continue
            buffers[path] = open(path, encoding="utf-8").read()
        n = buffers[path].count(old)
        if n != 1:
            failures.append(f"{tag}: 'old' found {n} times (must be exactly 1): {old[:80]!r}")
            continue
        buffers[path] = buffers[path].replace(old, new, 1)
        print(f"ok  {tag}  — {e.get('why', '')}")

    if failures:
        print("\nFAILED:")
        for x in failures:
            print("  " + x)
    print(f"\n{len(edits) - len(failures)}/{len(edits)} edits pass, {len(buffers)} file(s).")
    if failures:
        print("Nothing written. Fix or drop the failed edits and re-run.")
        return 1
    if not a.apply:
        print("Dry run. Re-run with --apply to write.")
        return 0
    for path, text in buffers.items():
        open(path, "w", encoding="utf-8").write(text)
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
