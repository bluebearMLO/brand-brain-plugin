# Index template → `00-README.md`

```markdown
# <Brand> Brand Brain: setup guide

Lives in `<path>`. One paragraph: what this is, the date built, what it was built from.
(Updates go in the Changelog at the bottom, not in this paragraph.)

## The <N> knowledge files
| File | What it gives Claude |
| `04-the-<slug>-system.md` | **Read first.** What the product is: ... |
| `01-brand-kit.md` | ... |
| `02-voice-rules.md` | ... |
| `03-brand-dna.md` | ... |
| `05-...` | ... (say if it names a never-print brand: "Never named in public copy.") |

## Set it up (5 minutes)
1. Step 1, Project: Claude → Projects → New project → "<Brand> Brand Brain".
2. Step 2, Brand kit: upload 01-brand-kit.md + logo files (exact paths) [+ brand book PDF].
3. Step 3, Voice: upload 02-voice-rules.md.
4. Step 4, Brand DNA: upload the system file and 03-brand-dna.md.
5. Step 4b, Knowledge: upload the 05+ files.
6. Step 4c, Plan and range: upload the short business plan, the roadmap and the range
   (exact paths; mark PROPOSED and internal-only items).
7. Project instructions: paste the block below.

(code block)
You are <Brand>'s in-house creative team. <Brand line / one-liner>.
The product: <one line from the system file>.
Before writing or designing anything, follow the project files: <system file> (what
the product is; read first), 01-brand-kit, 02-voice-rules, 03-brand-dna, <05+ with a
short gloss each>.
Rules: <spelling>. <2–3 voice traits>. Never invent <prices, dimensions, locations,
projects, reviews, stats>. All money figures are Estimates. <Partner rule: "built with",
nothing signed>. Never write <banned phrases>. Never name <never-print> in public text
or image prompts. <Imagery setting rule.> If a fact is not in the files, ask me
instead of guessing.
(end code block)

## Current source documents (<date>)
| Document | Path | Status |

**Superseded (do not use as a source):**
- <item>: replaced by <item>.

## Step 5: start creating (starter prompts)
6–9 prompts: channel work (social, web, email, B2B, image briefs), copy review against
voice + DNA, and one prompt per knowledge file.

## Open items to confirm
Numbered and dated. New items get the next number; resolved items are marked
**resolved <date>: <answer>**, not deleted.
1. **<Topic>:** <source A> says ..., <source B> says .... Files: ...

## Mind map
Pointer to the SVG (and Miro board if made).

## Changelog
- <YYYY-MM-DD> Built from <sources> (Build).
- <YYYY-MM-DD> <what changed> (Update / Rebuild R<n>).
```
