# Brand Brain: a Claude Code plugin

Turn any company's existing files into a **Brand Brain**: a Claude Project that knows the brand, so every chat produces on-brand ads, pages, posts and emails.

You point it at a project folder (or a website, or nothing, in which case it interviews you), and it writes:

| Output | What it is |
|---|---|
| `00-README.md` | Setup guide: how to create the Claude Project, project instructions to paste, starter prompts, open items to confirm |
| `01-brand-kit.md` | Logo, colour palette (hex), typography, UI rules, imagery, social kit, do/don't |
| `02-voice-rules.md` | How the brand sounds, set phrases, banned words, formatting, truth rules, gold-standard lines |
| `03-brand-dna.md` | Who we help, the problem, how we solve it, why we're different, proof, one line |
| `*-mindmap.svg` | One-page mind map of the whole brain (optionally a Miro board too) |
| `*-Brand-Brain.pdf` | Everything above in one branded PDF |

Every fact is traced to a source file, conflicts between sources are logged rather than guessed, and anything the brand can't prove goes on a "do not claim" list.

## Install (Claude Code)

```
/plugin marketplace add bluebearMLO/brand-brain-plugin
/plugin install brand-brain@brand-brain
```

Restart Claude Code afterwards if the skill doesn't show up.

## Use

Just ask, for example:

- `make the brand brain for Acme, the files are in ~/clients/acme`
- `build a brand brain for https://example.com`
- `we're starting a new brand called Northwind, interview me and build the brand brain`

Then follow the generated `00-README.md`: create a Claude Project, upload the three files and the logos, paste the project instructions, and start creating.

## Use in claude.ai (without Claude Code)

Zip the folder `plugins/brand-brain/skills/brand-brain/` and upload it under **Settings → Capabilities → Skills**. The PDF and mind-map scripts need a code-execution environment. Without one, the Markdown files are still produced.

## Requirements

- Python 3 (no extra packages)
- Google Chrome, Chromium or Edge, for the PDF (otherwise you get an HTML file to print)
- Optional: the Miro connector, for a Miro mind-map board

## How it works

It is the five-step Brand Brain method: **1 Project → 2 Brand kit → 3 Voice → 4 Brand DNA → 5 Create**. The skill does steps 2–4. When subagents are available, it runs those three in parallel, one subagent per file, each with a fixed template and the same ground rules:

- extract, don't invent;
- cite sources;
- log conflicts;
- verifiable proof only.

```
plugins/brand-brain/skills/brand-brain/
├── SKILL.md                 workflow
├── references/              templates for each file, interview prompts, mind-map schema
└── scripts/
    ├── mindmap.py           mindmap.json → SVG
    └── build_pdf.py         brand-brain folder → styled PDF (headless Chrome)
```

## Privacy

This repo holds only the method and templates. The Brand Brains it generates are written into your own project folders and are never published by the plugin. Keep client brand files out of public repos.

## License

MIT
