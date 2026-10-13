#!/usr/bin/env python3
"""Combine a Brand Brain folder into one styled PDF via headless Chrome/Chromium.

Usage:
  python3 build_pdf.py <brand-brain-dir> --title "Acme Brand Brain" [--tagline "..."]
      [--primary "#1c1d1b"] [--accent "#67422b"] [--paper "#f2eee7"] [--out file.pdf]

Order: cover (title, tagline, *mindmap.svg) -> 00-README.md -> 01-*.md -> 02-*.md -> 03-*.md,
each on a new page. No third-party Python packages needed. If no browser is found, the
HTML is left next to the PDF path for manual Print -> Save as PDF.
"""
import argparse
import glob
import html
import os
import re
import shutil
import subprocess
import sys


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"!\[(.*?)\]\((.*?)\)", r'<img alt="\1" src="\2">', t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"~~(.+?)~~", r"<s>\1</s>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<i>\1</i>", t)
    return t


LIST = re.compile(r"^(\s*)(- \[[ x]\] |[-*+] |\d+[.)] )")


def md_to_html(src):
    lines, out, i = src.split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            j, buf = i + 1, []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                buf.append(lines[j]); j += 1
            out.append("<pre>" + html.escape("\n".join(buf)) + "</pre>"); i = j + 1; continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i]); i += 1
            cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
            body = [r for r in rows[1:] if not re.match(r"^\|[\s:|-]+\|?$", r.strip())]
            head = "".join(f"<th>{inline(c)}</th>" for c in cells(rows[0]))
            trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(r)) + "</tr>" for r in body)
            out.append(f"<table><tr>{head}</tr>{trs}</table>"); continue
        m = re.match(r"(#{1,6}) (.*)", line)
        if m:
            n = len(m[1]); out.append(f"<h{n}>{inline(m[2])}</h{n}>")
        elif re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            out.append("<hr>")
        elif line.strip() == "PBREAK":
            out.append('<div class="pb"></div>')
        elif line.startswith(">"):
            out.append("<blockquote>" + inline(line.lstrip("> ")) + "</blockquote>")
        elif LIST.match(line):
            tag = "ol" if re.match(r"^\s*\d", line) else "ul"
            items = []
            while i < len(lines) and (LIST.match(lines[i]) or (lines[i].startswith("  ") and lines[i].strip() and items)):
                lm = LIST.match(lines[i])
                if lm:
                    text = lines[i][lm.end():]
                    box = "☐ " if "[ ]" in lm[2] else ("☑ " if "[x]" in lm[2] else "")
                    sub = ' class="sub"' if len(lm[1]) >= 2 else ""
                    items.append(f"<li{sub}>{box}{inline(text)}</li>")
                else:
                    items[-1] = items[-1][:-5] + " " + inline(lines[i].strip()) + "</li>"
                i += 1
            out.append(f"<{tag}>" + "".join(items) + f"</{tag}>"); continue
        elif line.strip():
            para = [line.strip()]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#|\||```|>|\s*([-*+]|\d+[.)]) |-{3,})", lines[i + 1]):
                i += 1; para.append(lines[i].strip())
            out.append("<p>" + inline(" ".join(para)) + "</p>")
        i += 1
    return "\n".join(out)


def find_browser():
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"):
        p = shutil.which(name)
        if p:
            return p
    for p in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if os.path.exists(p):
            return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--title", required=True)
    ap.add_argument("--tagline", default="")
    ap.add_argument("--primary", default="#1c1d1b")
    ap.add_argument("--accent", default="#8a5e3f")
    ap.add_argument("--paper", default="#f4f1ea")
    ap.add_argument("--out")
    a = ap.parse_args()
    d = os.path.abspath(a.dir)
    slug = re.sub(r"[^A-Za-z0-9]+", "-", a.title).strip("-")
    out_pdf = os.path.abspath(a.out or os.path.join(d, f"{slug}.pdf"))

    parts = [f"# {a.title}\n\n**{a.tagline}**\n\nBrand kit · Voice rules · Brand DNA, the knowledge files for the {a.title} Claude Project.\n"]
    mm = sorted(glob.glob(os.path.join(d, "*mindmap*.svg")))
    if mm:
        parts.append(f"![Mind map]({os.path.basename(mm[0])})\n")
    for pat in ("00-*.md", "01-*.md", "02-*.md", "03-*.md"):
        for f in sorted(glob.glob(os.path.join(d, pat))):
            text = open(f, encoding="utf-8").read()
            if pat == "00-*.md":
                text = re.sub(r"^# ", "## ", text, count=1, flags=re.M)
            parts.append("PBREAK\n\n" + text)
    body = md_to_html("\n\n".join(parts))

    css = f"""
    @page {{ margin: 16mm 14mm; }}
    body {{ font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; color: {a.primary}; max-width: 780px; margin: 0 auto; font-size: 10.5pt; line-height: 1.5; }}
    h1 {{ font-family: Georgia, serif; font-size: 28pt; margin: 0 0 6px; }}
    h2 {{ font-family: Georgia, serif; border-bottom: 2px solid {a.accent}; padding-bottom: 3px; margin-top: 22px; page-break-after: avoid; }}
    h3 {{ color: {a.accent}; page-break-after: avoid; }}
    img {{ max-width: 100%; max-height: 860px; display: block; margin: 12px auto; }}
    pre {{ background: {a.paper}; border-left: 4px solid {a.accent}; padding: 10px 14px; font-size: 9pt; white-space: pre-wrap; page-break-inside: avoid; }}
    code {{ background: {a.paper}; padding: 1px 4px; border-radius: 3px; font-size: 9pt; }}
    table {{ border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9pt; }}
    tr {{ page-break-inside: avoid; }}
    th {{ background: {a.primary}; color: #fff; text-align: left; padding: 5px; }}
    td {{ border-bottom: 1px solid #ddd; padding: 5px; vertical-align: top; }}
    blockquote {{ background: {a.paper}; margin: 10px 0; padding: 8px 12px; }}
    hr {{ border: none; border-top: 1px solid #ddd; margin: 16px 0; }}
    li.sub {{ margin-left: 22px; list-style: circle; }}
    .pb {{ page-break-after: always; }}
    a {{ color: {a.accent}; }}
    """
    page = f'<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(a.title)}</title><style>{css}</style></head><body>{body}</body></html>'
    tmp_html = os.path.join(d, "._brand-brain-print.html")  # same dir so relative images resolve
    open(tmp_html, "w", encoding="utf-8").write(page)

    browser = find_browser()
    if not browser:
        keep = out_pdf[:-4] + ".html"
        os.replace(tmp_html, keep)
        print(f"No Chrome/Chromium/Edge found. Open {keep} and use Print -> Save as PDF.")
        return 2
    subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf}", "file://" + tmp_html],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    os.remove(tmp_html)
    if not os.path.exists(out_pdf):
        sys.exit("PDF was not produced; try running the browser command manually.")
    print(f"wrote {out_pdf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
