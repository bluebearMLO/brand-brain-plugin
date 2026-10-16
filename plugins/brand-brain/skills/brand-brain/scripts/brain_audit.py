#!/usr/bin/env python3
"""Audit a Brand Brain folder against its brain.json manifest.

Usage:
  python3 brain_audit.py <brand-brain-dir> [--manifest path/to/brain.json] [--strict]

Checks (see references/manifest-schema.md):
  files     every read_order file exists and is named in 00-README.md
  paths     backticked paths in the brain resolve (lines saying removed / not in the
            repo / outside the repo are skipped, as are globs and placeholders)
  phrases   banned phrases and never-print names don't appear in the brain, except on
            lines that ban them; never-print names don't appear in public_paths at all
  register  superseded / not-source paths aren't cited outside 00-README.md's register
  locked    each locked line appears in the voice rules
  hygiene   open items numbered without duplicates; changelog mentions `updated`

Exit code 0 when clean, 1 when there are errors (warnings too, with --strict).
No third-party packages needed.
"""
import argparse
import glob
import json
import os
import re
import sys

NEGATION = re.compile(
    r"\b(never|not|don't|do not|no |avoid|banned|ban|instead of|retire|replace|rather than|"
    r"isn't|aren't|nor|without|stop|don’t|never print|wrong)\b", re.I)
SKIP_PATH_LINE = re.compile(r"removed|not in the repo|outside the repo|no longer|deleted|copy in ~", re.I)
PATH_LIKE = re.compile(r"`([^`\s][^`]*?)`")
EXTS = (".md", ".pdf", ".html", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".css", ".ts",
        ".tsx", ".json", ".xlsx", ".pptx", ".py", ".txt", ".docx")
TEXT_EXTS = (".md", ".mdx", ".html", ".tsx", ".ts", ".jsx", ".js", ".json", ".txt", ".yml", ".yaml")


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, area, msg):
        self.errors.append(f"[{area}] {msg}")

    def warn(self, area, msg):
        self.warnings.append(f"[{area}] {msg}")


def looks_like_path(s):
    if any(c in s for c in "*<>{}|[]") or s.startswith(("http", "#", "--", "$")) or " " in s.strip():
        return False
    return "/" in s or s.lower().endswith(EXTS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--manifest")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    d = os.path.abspath(a.dir)
    mpath = a.manifest or os.path.join(d, "brain.json")
    r = Report()

    if not os.path.exists(mpath):
        print(f"No manifest at {mpath}. Write brain.json (references/manifest-schema.md) first.")
        return 1
    m = json.load(open(mpath, encoding="utf-8"))
    root = m.get("project_root", ".")
    root = root if os.path.isabs(root) else os.path.normpath(os.path.join(d, root))

    readme_path = os.path.join(d, "00-README.md")
    readme = open(readme_path, encoding="utf-8").read() if os.path.exists(readme_path) else ""
    if not readme:
        r.err("files", "00-README.md is missing")

    brain_files = sorted(glob.glob(os.path.join(d, "[0-9][0-9]-*.md")))
    texts = {os.path.basename(f): open(f, encoding="utf-8").read() for f in brain_files}

    # files
    for f in m.get("read_order", []):
        if f not in texts:
            r.err("files", f"read_order file missing: {f}")
        elif f not in readme:
            r.err("files", f"{f} is not named in 00-README.md")
    for f in texts:
        if f != "00-README.md" and f not in m.get("read_order", []):
            r.warn("files", f"{f} exists but is not in read_order")
    for k, p in (m.get("authorities") or {}).items():
        if p and not os.path.exists(os.path.join(root, p)):
            r.err("paths", f"authority '{k}' not found: {p}")
    for p in m.get("agents", []):
        if not os.path.exists(os.path.join(root, p)):
            r.err("files", f"agent file not found: {p}")

    # paths: resolve against the project root, the brain folder, the root's parent (sibling
    # projects) and, failing those, any file under the root whose path ends with the citation
    # (brains often cite paths relative to a sub-folder named nearby).
    index = None

    def resolves(s):
        nonlocal index
        cands = [os.path.join(root, s), os.path.join(d, s), os.path.join(os.path.dirname(root), s),
                 os.path.expanduser(s)]
        if any(os.path.exists(c) for c in cands):
            return True
        if index is None:
            index = []
            for dp, dns, fns in os.walk(root):
                dns[:] = [x for x in dns if x not in ("node_modules", ".next", ".git", "dist", ".venv")]
                index.extend(os.path.join(dp, x) for x in fns + dns)
        suffix = os.sep + s.strip("/")
        return any(p.endswith(suffix) for p in index)

    missing = {}
    for name, text in texts.items():
        for ln, line in enumerate(text.splitlines(), 1):
            if SKIP_PATH_LINE.search(line):
                continue
            for s in PATH_LIKE.findall(line):
                s = s.strip().rstrip(".,;:")
                if not looks_like_path(s):
                    continue
                s_clean = s.split("#")[0].split(" (")[0]
                if "/" not in s_clean:
                    continue  # bare file names are too ambiguous to fail on
                if s_clean.startswith("/") and s_clean.count("/") == 1 and "." not in s_clean:
                    continue  # a site route like /about
                if not resolves(s_clean):
                    missing.setdefault(s_clean, []).append(f"{name}:{ln}")
    for p, where in sorted(missing.items()):
        r.warn("paths", f"not found: {p}  ({', '.join(where[:3])}{' …' if len(where) > 3 else ''}); "
                        "fix it, or mark the line (removed) / (not in the repo)")

    # phrases
    def scan(words, kind, allow_bans=True):
        for w in words:
            pat = re.compile(re.escape(w), re.I)
            for name, text in texts.items():
                lines = text.splitlines()
                for ln, line in enumerate(lines, 1):
                    context = (lines[ln - 2] if ln > 1 else "") + " " + line
                    if pat.search(line) and not (allow_bans and NEGATION.search(context)):
                        yield name, ln, w, line.strip()

    for name, ln, w, line in scan(m.get("banned_phrases", []), "banned"):
        r.warn("phrases", f"banned phrase '{w}' at {name}:{ln}: {line[:110]}")
    # never_print names are expected inside the brain (it must say what to avoid); only
    # flag them in files that aren't knowledge files about them.
    for p in m.get("public_paths", []):
        base = os.path.join(root, p)
        files = [base] if os.path.isfile(base) else [
            os.path.join(dp, fn) for dp, dns, fns in os.walk(base)
            if not any(x in dp for x in ("node_modules", ".next", ".git", "dist"))
            for fn in fns if fn.endswith(TEXT_EXTS)]
        for fp in files:
            try:
                t = open(fp, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            for w in m.get("never_print", []):
                for mt in re.finditer(re.escape(w), t, re.I):
                    ln = t.count("\n", 0, mt.start()) + 1
                    r.err("phrases", f"never-print '{w}' in public file {os.path.relpath(fp, root)}:{ln}")

    # register
    srcs = m.get("sources", {})
    retired = [(s["path"], "superseded") for s in srcs.get("superseded", [])] + \
              [(p, "not a source") for p in srcs.get("not_sources", [])]
    for p, why in retired:
        for name, text in texts.items():
            if name == "00-README.md":
                continue
            for ln, line in enumerate(text.splitlines(), 1):
                if p in line and not re.search(r"supersed|replaced|old |no longer|not a source|brief", line, re.I):
                    r.warn("register", f"{why} source cited at {name}:{ln}: {p}")

    # locked lines
    voice = next((t for n, t in texts.items() if "voice" in n), "")
    norm = lambda s: re.sub(r"[\s“”\"'’]+", " ", s).strip().lower()
    for line in m.get("locked_lines", []):
        if norm(line) not in norm(voice):
            r.warn("locked", f"locked line not in voice rules: {line}")

    # hygiene
    sec = re.search(r"^## Open items.*?(?=^## |\Z)", readme, re.M | re.S)
    if sec:
        nums = re.findall(r"^\s*(?:\*\*)?(\d+[a-z]?)\.", sec.group(0), re.M)
        dup = sorted({n for n in nums if nums.count(n) > 1})
        if dup:
            r.warn("hygiene", f"open items numbered twice: {', '.join(dup)}")
    else:
        r.warn("hygiene", "no '## Open items' section in 00-README.md")
    upd = m.get("updated")
    if upd and upd not in readme:
        r.warn("hygiene", f"README never mentions the manifest's updated date {upd} (add a changelog line)")
    if "## Changelog" not in readme:
        r.warn("hygiene", "no '## Changelog' section in 00-README.md")

    for x in r.errors:
        print("ERROR " + x)
    for x in r.warnings:
        print("warn  " + x)
    print(f"\n{len(r.errors)} error(s), {len(r.warnings)} warning(s) in {len(texts)} brain file(s); root {root}")
    return 1 if r.errors or (a.strict and r.warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
