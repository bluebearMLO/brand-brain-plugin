# Brand Brain: a Claude Code plugin

Turn any company's existing files into a **Brand Brain**: a Claude Project that knows the brand, so every chat produces on-brand ads, pages, posts and emails. The plugin also keeps the brain correct as the business plan, research and owner decisions change.

It has four modes:

| Mode | Use it when | Ask, for example |
|---|---|---|
| **Build** | No brain exists yet | `make the brand brain for Acme, the files are in ~/clients/acme` |
| **Update** | A new plan, report, range or decision arrived | `fold the new business plan into the Acme brain` |
| **Rebuild** | The brain is wrong about something basic, or you want it redone | `the brain is wrong: the frame is ours, not a supplier's. Rebase it` / `rebuild the Acme brain from scratch` |
| **Audit** | Before handing it over, or any time | `audit the Acme brain` |

A build writes:

| Output | What it is |
|---|---|
| `00-README.md` | Index: Claude Project setup, project instructions to paste, **source register** (current vs superseded plan, roadmap, research), starter prompts, open items, changelog |
| `04-the-<brand>-system.md` | **Read first.** What the product actually is: its parts, who makes and supplies each, how it's made, what may and may not be said |
| `01-brand-kit.md` | Logo, colour palette (hex), typography, UI rules, imagery, do/don't |
| `02-voice-rules.md` | How the brand sounds, locked lines, banned words, formatting, truth rules, gold-standard lines |
| `03-brand-dna.md` | Who we help, the problem, how we solve it, why we're different, proof, one line |
| `05+` knowledge files | Only when the sources support them: technical design standards, a design benchmark (never named in public), regulated-claims rules |
| `brain.json` | Manifest: read order, authorities, source register, never-print names, banned phrases, owner corrections, agents |
| `.claude/agents/<brand>-*.md` | Optional project agent team (brand guardian, business analyst, buyer advocate, 1–2 domain experts) that return reviewable edits |
| `*-mindmap.svg` | One-page mind map of the whole brain (optionally a Miro board too) |
| `*-Brand-Brain.pdf` | Everything above in one branded PDF |

Every fact is traced to a source file. Conflicts between sources are logged rather than guessed. Anything the brand can't prove goes on a "do not claim" list. Owner corrections are recorded once in `brain.json`, beat every older document, and survive every rebuild.

## Install (Claude Code)

```
/plugin marketplace add bluebearMLO/brand-brain-plugin
/plugin install brand-brain@brand-brain
```

Restart Claude Code afterwards if the skill doesn't show up.

## Use

Ask in plain words (see the modes table above). It also works from a website (`build a brand brain for https://example.com`) or from nothing (`we're starting a new brand called Northwind, interview me and build the brand brain`).

After a build, follow the generated `00-README.md`: create a Claude Project, upload the three files and the logos, paste the project instructions, and start creating.

## Use in claude.ai (without Claude Code)

Zip the folder `plugins/brand-brain/skills/brand-brain/` and upload it under **Settings → Capabilities → Skills**. The PDF and mind-map scripts need a code-execution environment. Without one, the Markdown files are still produced.

## Requirements

- Python 3 (no extra packages)
- Google Chrome, Chromium or Edge, for the PDF (otherwise you get an HTML file to print)
- Optional: the Miro connector, for a Miro mind-map board

## How it works

It is the five-step Brand Brain method: **1 Project → 2 Brand kit → 3 Voice → 4 Brand DNA → 5 Create**, with two additions learned on real brains:

- **System file first.** Before the kit, voice and DNA are written, one file pins down what the product actually is. The costliest brain error is a wrong idea of the product.
- **Sources have a status.** Business plans, roadmaps and research supersede each other. The index says which document is current, which part of it, and what replaced the rest.

When subagents are available, the kit, voice, DNA and knowledge files are written in parallel, one subagent per file, each with a fixed template and the same ground rules:

- extract, don't invent;
- cite sources;
- log conflicts;
- owner corrections win;
- PROPOSED is never presented as settled;
- verifiable proof only; money is an Estimate.

```
plugins/brand-brain/skills/brand-brain/
├── SKILL.md                 the four modes
├── references/              templates (system, kit, voice, DNA, knowledge files, index),
│                            source register, manifest schema, rebuild protocol, agent team,
│                            interview prompts, mind-map schema
└── scripts/
    ├── brain_audit.py       brain.json → consistency report (files, paths, phrases, register)
    ├── apply_edits.py       agent JSON edits → files (dry run, all-or-nothing)
    ├── mindmap.py           mindmap.json → SVG
    └── build_pdf.py         brand-brain folder → styled PDF in read order (headless Chrome)
```

## Privacy

This repo holds only the method and templates. The Brand Brains it generates are written into your own project folders and are never published by the plugin. Keep client brand files out of public repos.

## License

MIT
