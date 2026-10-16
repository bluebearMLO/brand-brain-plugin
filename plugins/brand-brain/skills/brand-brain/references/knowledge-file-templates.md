# Knowledge files (`05+`): when to make one, and templates

Make a knowledge file only when the sources hold real domain knowledge that Claude would otherwise get wrong, and when it is too big to sit in 03 or the system file. Each one gets a number, a line in the README files table, a place in `brain.json` `read_order`, and a starter prompt that uses it.

Every knowledge file opens with **How to use it**: what it is, what it is not, and the never-print rules that apply.

## A. Technical standards → `NN-<domain>-design-standards.md`

When: build guides, codes, engineering reports, lab or formulation notes, or industry handbooks exist.

Rules:
- These are **design standards and industry rules, not product specs**. A number here says what good design requires, not what a product is, until that product's spec is confirmed.
- In marketing, use them to explain **principles** ("benches set so your feet rest above the stones"), never as performance claims.
- Defer to the component maker's manual and local code where they differ, and name which code.

```markdown
# NN — <Brand> <domain> design standards (technical knowledge)
How to use it: ...
Source keys: [A] ... [B] ...
## 1. Rules all sources agree on (safe to design to)
| Rule | Value / range | Sources |
## 2. Where the sources disagree (<Brand> must decide)
| Topic | Option 1 (sources) | Option 2 (sources) | Recommendation (PROPOSED) |
## 3. The <Brand> product-sheet standard (what every spec sheet should publish)
## 4. Numbers for planning (formulas, sizing tables)
## 5. What this means for <Brand>'s story (principles we can say; claims we can't)
## 6. Where to read more (paths)
```

## B. Design benchmark → `NN-<benchmark-slug>-design-reference.md`

When: there is a teardown, catalogue or assessment of the brand the design language is measured against.

Rules:
- The benchmark is a **reference and a competitor**, never a partner or a source of claims about the brand.
- **Add it to `brain.json` → `never_print`.** Never name it in public copy or image prompts, and never compare publicly ("better than X").
- Its dimensions, capacities and prices are its own. Never reuse them as the brand's specs.
- If the benchmark shares a parent, supplier or partner with the brand, be neutral about both and imply no endorsement.

```markdown
# NN — <Benchmark>: <Brand>'s main design reference
Rules for using this file: ...
## 1. The verdict in one paragraph
## 2. The range (table, with scores if an assessment exists)
## 3. What it does well (<Brand> should match)
## 4. Where it falls short (<Brand> must beat)
## 5. The ideas <Brand> takes (ranked, each with where it applies)
## 6. The <Brand> standard that follows
## 7. How to use this in work (prompts and review checklists)
```

## C. Range / catalogue

When a range document exists, the brain **points to it** (in the source register and the system file's plan section) rather than copying it, especially while it is PROPOSED. Copy into a knowledge file only a stable, approved range, as a table of names, one-line role, status and source. Never invent sizes or prices.

## D. Regulated claims → `NN-claims-and-compliance.md`

When the category has wording rules: health and wellness, food, finance, building safety, environmental claims.

```markdown
## 1. Words we can't use, and the legal reason (fireproof, cures, guaranteed, eco-friendly…)
## 2. Approved wording for common claims
## 3. Certifications held (with evidence path) / not held
## 4. Who signs off what
```
