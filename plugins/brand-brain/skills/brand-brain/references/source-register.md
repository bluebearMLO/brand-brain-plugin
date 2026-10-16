# Source register: inventory, authorities, current vs superseded

A brain is only as good as its idea of which document is current. Projects pile up versions: a brand book, then a website, then research, then a business plan that overrides half the research, then an owner decision that overrides part of the plan. The register makes that explicit.

## 1. Where to look

| Kind | Typical places |
|---|---|
| Identity | brand book / production deck PDF or PPTX, `DESIGN.md`, `globals.css` / theme tokens, `public/*logo*`, Figma exports |
| Claims | `PRODUCT.md`, capability statement, spec sheets, engineering reports, `CLAUDE.md`/`AGENTS.md` rules |
| Business | `business-plan/` (full, short, deck), `ROADMAP.md`, `FINANCIALS.md` or a model `.xlsx`, `PLANS.md`, research report folders (market, customers, competitors, pricing, cost, supply chain, manufacturing, regulatory, go-to-market, pilot, financial plan, risks, target markets) |
| Copy | site pages and components, journal/blog, emails, social captions and guides |
| Technical / reference | build guides, standards, benchmark teardowns, competitor reports |
| Owner word | owner-written rules files (plain-words rules, format decisions), dated correction briefs |

A research folder usually has a `README.md` index with headlines. Read that first, then only the executive summaries, and open the full reports only for the facts you need.

## 2. The four authorities

| Authority | Decides | Usual pick |
|---|---|---|
| Identity | logo, colour, type, imagery | brand book / deck; else the most deliberate design doc; last resort shipped tokens (say so) |
| Claims | what may be stated as fact | the most formal published product document |
| Plan | prices, money, range, business model | the current business plan |
| Calendar | launch dates and sequence | the roadmap, if the plan has one; else the plan |

When the plan authority and the research disagree, the plan wins and the research figure is marked superseded on that point. Research is still good evidence for *why*.

## 3. Statuses

| Status | Meaning | How the brain uses it |
|---|---|---|
| **Current** | Use it | Cite it; upload it to the Claude Project if useful |
| **Current, only part X** | Only one section is current (e.g. "only the final CURRENT NUMBERS section") | Cite only that part; say so in the register |
| **PROPOSED** | Drafted, owner hasn't approved | Point to it; never present it as settled; internal only if it names never-print brands |
| **Superseded** | Replaced | List under "Superseded (do not use as a source)" with what replaced it |
| **Not a source** | Writer briefs, prompts, handover notes | List them so nobody cites them |
| **Removed / outside repo** | Was cited, file is gone or elsewhere | Keep the rule it gave; mark the path `(removed)` or `(not in the repo)` so the audit skips it |

## 4. Writing it into the README

```markdown
## Current source documents (<date>)
| Document | Path | Status |

**Superseded (do not use as a source):**
- <old thing>: replaced by <new thing> (<date or decision>).
- <doc>, every section before "<heading>".
- <writer briefs>: briefs, not sources.
```

Mirror the same lists in `brain.json` → `sources`.

## 5. Typical things that get superseded

- An old product line-up on the website after a new range is drafted.
- An older raise or launch date in research after the plan settles the money and dates.
- Earlier scenarios in a financials file once a final scenario is chosen.
- A settled-facts calendar inside a brief once a roadmap exists.
- Old image prompts that break the current imagery rules.
