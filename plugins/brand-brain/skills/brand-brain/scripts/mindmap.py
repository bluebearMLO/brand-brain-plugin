#!/usr/bin/env python3
"""Render a Brand Brain mind map (root -> branches -> leaves) to a standalone SVG.

Usage: python3 mindmap.py mindmap.json out.svg
Schema: see references/mindmap-schema.md
"""
import html
import json
import sys
import textwrap


def luminance(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def main(src, out):
    d = json.load(open(src))
    bg = d.get("background", "#f7f5f0")
    root_fill = d.get("root_color", "#1c1d1b")
    root_text = d.get("root_text", "#ffffff")
    ink = d.get("ink", "#1c1d1b")
    leaf_fill = d.get("leaf_fill", "#ffffff")

    LW, LH, GAP, GROUP_GAP, PAD = 560, 84, 16, 56, 60
    X0, X1, X2, RW, BW = 40, 520, 920, 360, 300

    y, branches = 0, []
    for b in d["branches"]:
        ys = [y + i * (LH + GAP) for i in range(len(b["leaves"]))]
        h = ys[-1] + LH - y
        branches.append((b, ys, y + h / 2))
        y += h + GROUP_GAP
    total = y - GROUP_GAP

    W, H = X2 + LW + PAD, total + 2 * PAD + 90
    oy = PAD + 70
    ry = oy + total / 2
    e = lambda s: html.escape(str(s))
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica, Arial, sans-serif"><rect width="100%" height="100%" fill="{bg}"/>',
         f'<text x="{X0}" y="54" font-family="Georgia, serif" font-size="30" fill="{ink}">{e(d["title"])} · mind map</text>']

    for b, ys, cy in branches:
        c = b["color"]
        o.append(f'<path d="M{X0+RW},{ry} C{X0+RW+60},{ry} {X1-60},{oy+cy} {X1},{oy+cy}" stroke="{c}" stroke-width="3" fill="none"/>')
        for ly in ys:
            o.append(f'<path d="M{X1+BW},{oy+cy} C{X1+BW+50},{oy+cy} {X2-50},{oy+ly+LH/2} {X2},{oy+ly+LH/2}" '
                     f'stroke="{c}" stroke-width="2" fill="none" opacity=".7"/>')

    o.append(f'<rect x="{X0}" y="{ry-70}" width="{RW}" height="140" rx="4" fill="{root_fill}"/>'
             f'<text x="{X0+RW/2}" y="{ry-6}" text-anchor="middle" font-family="Georgia, serif" font-size="30" fill="{root_text}">{e(d["title"])}</text>'
             f'<text x="{X0+RW/2}" y="{ry+32}" text-anchor="middle" font-size="17" fill="{root_text}" opacity=".7">{e(d.get("tagline",""))}</text>')

    for b, ys, cy in branches:
        c = b["color"]
        tc = "#ffffff" if luminance(c) < 0.45 else ink
        o.append(f'<rect x="{X1}" y="{oy+cy-36}" width="{BW}" height="72" rx="4" fill="{c}"/>'
                 f'<text x="{X1+24}" y="{oy+cy+9}" font-family="Georgia, serif" font-size="26" fill="{tc}">{e(b["name"])}</text>')
        for t, ly in zip(b["leaves"], ys):
            o.append(f'<rect x="{X2}" y="{oy+ly}" width="{LW}" height="{LH}" rx="4" fill="{leaf_fill}" stroke="{c}" stroke-width="1.5"/>')
            lines = textwrap.wrap(t, 58)[:3]
            sy = oy + ly + LH / 2 - (len(lines) - 1) * 11 + 6
            for k, line in enumerate(lines):
                o.append(f'<text x="{X2+18}" y="{sy+k*22}" font-size="17" fill="{ink}">{e(line)}</text>')

    o.append("</svg>")
    open(out, "w").write("\n".join(o))
    print(f"wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
