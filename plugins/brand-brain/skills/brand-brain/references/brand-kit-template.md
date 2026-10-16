# Brand kit template → `01-brand-kit.md`

> Read the system file (`04-the-<slug>-system.md`, or whichever file `brain.json` lists first) before writing this one. Where you disagree with it on what the product is, it wins. Owner corrections in `brain.json` → `corrections` win over every source.

Fill this structure from the sources. Delete a section only if the brand truly has nothing for it, and say so in one line (`No motion rules defined yet.`). Cite sources per section.

```markdown
# <Brand> Brand Brain — 01 Brand kit

Knowledge file for the <Brand> Brand Brain Claude Project. Visual identity only.
Compiled <YYYY-MM-DD> from the sources below. Identity authority: <brand book / deck>.

Source keys: [DECK] path · [DESIGN] path · [CSS] path · ...

## 1. Logo
- The mark and what it means; lockups/variants with file paths
- Colourways; clear space; minimum size; placement
- Misuse (don't stretch, recolour, add effects, ...)
Source: ...

## 2. Colour palette
| Name | Hex | Meaning / role | Use on |
|---|---|---|---|
### UI extensions (tints from code tokens, if any)
### Usage ratios (sourced, or "not specified; guidance: ...", labelled as interpretation)

## 3. Typography
| Role | Typeface (brand) | Shipped / fallback | Weights | Notes |
Type scale if defined (H1..body..caption, sizes, line-height, tracking).
Licensing status, if any faces are stand-ins.

## 4. UI components, layout and motion
Buttons, links, cards, fields, nav, radius, borders/shadows, spacing scale, grid, breakpoints, motion.

## 5. Photography and imagery
Subject, light, materials, palette, framing, people/no people, what to avoid.
How concept/AI imagery must be labelled.
Image-generation briefs (2–3 when real photography is thin): aspect ratio, suggested file path, an art-director prose brief ending "no text, no logos, no watermarks".

## 6. Channel assets (only if the sources contain them)
Include this section only when the project's own sources hold real channel assets
(a social kit, templates, handles). Never create it from material in another project
or from a generic expectation that brands have one. If nothing exists, leave the
section out; don't write "none yet".

## 7. Do / Don't
Two short bullet lists.

## 8. Quick tokens (copy-paste)
A code block of hex + font tokens.

## 9. Source conflicts register
| Topic | Source A says | Source B says | Resolution / owner to confirm |
```
