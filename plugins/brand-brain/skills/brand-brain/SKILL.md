---
name: brand-brain
description: Build, update, rebuild or audit a "Brand Brain" for a company, brand or project, meaning the knowledge files that go into a Claude Project so every chat produces on-brand, truthful work. These are the system file (what the product really is), Brand kit, Voice rules, Brand DNA and optional knowledge files (technical standards, design benchmark), plus an index tied to the business plan, roadmap and research. It can also set up a project agent team to keep the brain correct, a mind map and a PDF. Use this whenever someone wants to capture a brand for Claude, make Claude write or design "on brand", set up a brand Claude Project, or distil guidelines, voice or positioning from existing files. Also use it when they want to fold a new document, business plan or owner correction into an existing brain, or rebuild or re-check one. Triggers include "make the brain for X", "brand brain", "update the brain", "rebuild the brain", "rebase the brain on…", "the brain is wrong about…", "audit the brain", even if they don't name the skill. It works from a folder of brand material, a website, or an interview when nothing exists yet.
---

# Brand Brain

A Brand Brain is a folder of knowledge files that goes into a Claude Project, so every chat started there already knows the brand. Getting the facts right matters more than polish. A brain that invents a statistic or a price will repeat it in every ad it writes, and a brain that is right on day one but never updated will repeat yesterday's plan.

The skill has four modes. Pick one in step 0.

| Mode | When | What happens |
|---|---|---|
| **Build** | No brain exists yet | Full pipeline: sources → system file → kit/voice/DNA → knowledge files → index → agents → mind map → PDF |
| **Update** | A brain exists; a new document, plan, report or decision arrived | Fold it in: repoint sources, edit only affected sections, log it |
| **Rebuild** | The owner says the brain is wrong about something basic ("the product is actually…"), or asks to redo it | Record the correction as owner truth, then re-derive every file against it; optionally from scratch with the old brain archived |
| **Audit** | "Check the brain", or before handing it over | Run `scripts/brain_audit.py` and a read-through; report and fix drift |

## The files

| File | Answers | Made |
|---|---|---|
| `00-README.md` | Index: setup steps, project instructions, **source register** (current vs superseded), open items, changelog | Always |
| `01-brand-kit.md` | What it looks like: logo, colours (hex), type, UI, imagery, do/don't | Always |
| `02-voice-rules.md` | How it sounds: traits, locked lines, banned words, formatting, truth rules | Always |
| `03-brand-dna.md` | Who it's for and why it wins: customer, problem, solution, difference, proof | Always |
| `04-the-<slug>-system.md` | **Read first.** What the product actually is: parts, who supplies what, how it's made, message hierarchy, what may be said | Always, unless the brand is so simple that a short section in 03 covers it |
| `05+` knowledge files | Domain knowledge Claude needs to be right: technical standards, a design benchmark, a regulated-claims file, a range or catalogue | Only when sources support one (see `references/knowledge-file-templates.md`) |
| `brain.json` | Machine-readable manifest: read order, authorities, source register, never-print names, banned phrases, owner corrections, agents | Always; drives audits and rebuilds |
| `*-mindmap.svg`, `*-Brand-Brain.pdf` | One-page map and one bound PDF | Always |

**Numbering:** in an existing brain, never renumber files. Owners and other files cite them by number. New files take the next free number, and the README and `brain.json` `read_order` say which one to read first. (A brain that grew its system file later may have it as `06`. That is fine.)

## Ground rules (copy word for word into every subagent prompt)

- Extract; don't invent. Every hex code, font, tagline, number and claim must come from a source. Add a short `Source:` line or `[KEY]` tag to each section.
- When sources disagree, the identity authority wins on look, the claims authority wins on facts, and the plan authority wins on dates, prices and money. Record every conflict in the file's conflicts table rather than silently picking one. Code-vs-docs disagreements are **owner call**.
- **Owner corrections beat every document.** Anything in `brain.json` → `corrections` is settled truth, even if an older source says otherwise. Mark the older source superseded on that point; never "balance" the two.
- Give each rule a status where it's in doubt: **followed** (existing copy does it), **wish** (stated but not followed), **owner call** (undecided), **PROPOSED** (drafted by Claude or an agent, owner to approve). Never present a PROPOSED item as settled.
- Names that must never appear in public (a benchmark competitor, a supplier, a machine brand, a client under NDA) can be named inside the knowledge files so Claude knows what to avoid. Put them in a clearly headed "Never print" list.
- Hex codes and font names go in plain text, not only in images.
- Proof is only what can be verified. Give "proof we don't have yet / do not claim" its own list: prices, dimensions, client names, reviews, stats, awards, partnerships, certifications that aren't in the sources.
- Money from plans and models is an **Estimate** unless the source says it is a quoted or invoiced figure. Say so wherever a figure appears.
- Partners or suppliers with no signed agreement are described as "built with" / "uses", never "official partner", "dealer" or "endorsed by".
- Quote real lines verbatim, with their file path, as gold-standard examples.
- Plain, direct language. No slogans or metaphors in the knowledge files themselves.
- Keep each file dense and scannable: 120–300 lines of tables and short bullets.
- Use only this project's sources. Never pull rules, assets or sections from another project's files, even a related one, and never add a section just because brands usually have one.
- Only write your own file.

## Mode: Build

### 0. Scope the job

Work out these points, and ask only if they aren't clear from the request:
- **Target:** a local folder (best), a website URL, uploaded files, or nothing (interview mode).
- **Brand name** and a short **slug** (`acme`, `northwind`).
- **Output folder:** suggest `<target>/soldoc/brand/brand-brain/` if a `soldoc/` docs folder exists, else `<target>/brand-brain/` (or `./brand-brain-<slug>/` with no folder), and confirm it. Writing into a repo can break that repo's own rules, so read its `CLAUDE.md`/`AGENTS.md` first. Never write into the user's Desktop root.
- **Mode check:** if a `brain.json` or `00-README.md` already exists there, this is not a build. Switch to Update or Rebuild.

### 1. Inventory the sources and fix the authorities

Rank everything before reading deeply. Read `references/source-register.md` for the full method. In short:

- **Identity sources:** brand books, production decks (PDF/PPTX), design-system docs, tokens (`globals.css`, theme files), logo files.
- **Claims sources:** capability statements, `PRODUCT.md`, spec sheets, engineering documents, plans.
- **Business sources:** the business plan (full, short, deck), roadmap, financial model, research reports, market and competitor reports. These decide dates, prices, the launch sequence and the range. They are often the biggest change since the brand book was written.
- **Written copy:** site pages, journal posts, emails, social captions.
- **Technical and reference material:** build guides, standards, benchmark teardowns.

Skip `node_modules`, `.next`, `dist`, `.git`, `.venv` and lock files. For a website, scrape home, about, product and blog pages.

Decide and write down four **authorities**: **identity** (look), **claims** (what may be stated as fact), **plan** (dates, prices, money, range) and **calendar** (one document that owns the launch dates, usually the roadmap). Then sort every business document into **current**, **current, only part X** (for example "only the final scenario section of FINANCIALS.md"), **PROPOSED** or **superseded**. Writer briefs, prompts and handover notes are **not sources**. List them as such.

**Pre-read before delegating.** Skim the key sources yourself. Extract big PDFs and decks once to text files in a scratch folder and pass those paths on. Note key facts and conflicts you've already spotted. The ranked list, the four authorities, the key facts, the known conflicts and any owner corrections go into every subagent brief.

### 2. Write the system file first

Write `04-the-<slug>-system.md` yourself, or with one subagent, from `references/system-template.md`, **before** the other files. It defines what the product is (its parts, who makes and supplies each, how it's assembled, the message hierarchy, what may and may not be said), so the kit, voice and DNA all sit on the same foundation. The most expensive mistake in a brain is a wrong idea of the product, such as calling an in-house component a bought-in part, or a partner a supplier. If the sources leave the product definition unclear, **stop and ask the owner** before going on.

### 3. Build kit, voice and DNA (in parallel if you can)

If an Agent/subagent tool is available, start three subagents in one message, one per file. Give each:
- brand name, project root, output path;
- the ranked sources (with pre-extracted text paths), the four authorities, key facts, known conflicts;
- the system file path, with "read it first; where you disagree with it, it wins on what the product is";
- its template from `references/` (`brand-kit-template.md`, `voice-rules-template.md`, `brand-dna-template.md`);
- the ground rules, word for word.

Some harnesses block subagents from writing `.md` files. If a write fails, have the subagent return the full file text in its final message and write it yourself. Without subagents, do the three files one after another.

### 4. Knowledge files (only where the sources support them)

Read `references/knowledge-file-templates.md` and decide which, if any, apply:
- **Technical standards:** the domain rules the product is designed to (from build guides, codes, standards, engineering reports). They are principles, never product specs.
- **Design benchmark:** the brand the design language is measured against. It covers what to match, where to beat it, and the ideas to take. The benchmark goes on the never-print list.
- **Range / catalogue:** only when a range document exists. Point at it rather than copying it if it is still PROPOSED.
- **Regulated claims:** health, finance, safety or environmental wording rules, when the category has them.

Run them as extra parallel subagents with the same brief. Fold their key findings back into 03 (difference, proof) and the system file (build-up, what may be said).

### 5. Fill gaps by interview (only what's missing)

- **No visual identity:** design-system prompt in `references/interview-prompts.md`. Everything it produces is **PROPOSED** until the owner approves.
- **No written copy:** the voice interview in the same file.
- **No positioning:** go through the 6 Brand DNA lines with the owner one at a time.
- **Unclear product definition:** ask, with the specific options you found in the sources.

Ask in one batch. If the user wants a draft now, use clearly labelled `[TO CONFIRM]` placeholders.

### 6. Index `00-README.md` and manifest `brain.json`

Use `references/readme-template.md` and `references/manifest-schema.md`. The README must include:
- the files table, with the system file marked **Read first**;
- Claude Project setup, step by step, with exact paths of logos and of the business documents to upload alongside (short plan, roadmap, range), and which ones are internal only;
- **project custom instructions** ready to paste. They must name the read-first file and carry the truth rules, the never-print names, the banned phrases and the "ask if a fact isn't in the files" rule;
- the **source register**: current documents, with status and path, then a **Superseded (do not use as a source)** list, each item with what replaced it;
- starter prompts suited to this brand's channels and knowledge files;
- **open items to confirm**: every conflict and gap, numbered and dated, with the files involved;
- a **changelog**: one dated line per build, update or rebuild.

`brain.json` must agree with the README. The audit checks that it does.

### 7. Agent team (offer it; default yes on a build in a code repo)

A brain decays as plans change. A small set of project agents keeps it in line. Read `references/agent-team.md`. Propose the team, then write `<root>/.claude/agents/<slug>-*.md` once the user agrees:
- **brand guardian:** voice, claims, names, visual rules, image prompts; owns 00–03;
- **business analyst:** keeps the brain in line with the plan, roadmap, prices and financial model;
- **buyer advocate:** reviews the range and the copy as the real buyer segments from 03 would;
- **1–2 domain experts** derived from the system file (for a sauna on a steel frame: a sauna architect and a steel engineer; for a skincare brand: a formulation chemist and a regulatory reviewer).

Each agent shares the same "How you work" block, which states the core product facts and the edit protocol (return JSON edits, never write the files). Record the agents in `brain.json`.

### 8. Mind map

Write `mindmap.json` (schema in `references/mindmap-schema.md`): the brand at the root, then branches for System, Brand kit, Voice rules, Brand DNA, Knowledge (if any) and Create, each with 3–5 short leaves taken from the files. Use the brand colours. Then run:

```bash
python3 <skill-dir>/scripts/mindmap.py <out>/mindmap.json <out>/<Brand>-Brand-Brain-mindmap.svg
```

Look at the SVG: no clipped text and no empty branches. **Miro (optional):** if Miro is connected and the user wants a board, build the same tree there (`canvas_get_canvas_composer_skill`, then `free_form`). Confirm before creating it, because the board is visible to the user's team.

### 9. PDF

```bash
python3 <skill-dir>/scripts/build_pdf.py <out> --title "<Brand> Brand Brain" --tagline "<brand line>" --primary "#hex" --accent "#hex" --paper "#hex"
```

It binds the mind map, `00-README.md` and every `NN-*.md` file, in the `brain.json` read order when one exists. Render a page or two (`pdftoppm`) and look at them before saying it's done. With no browser it leaves an HTML file to print.

### 10. Audit, then report

Run `python3 <skill-dir>/scripts/brain_audit.py <out>` and fix what it finds (see Mode: Audit). Then reply briefly:
- output folder and a table of files;
- the product in one line, from the system file, and the 6-line Brand DNA, the quickest checks that you understood the brand;
- the most important open items and conflicts;
- any image-slot prompts (with path and aspect ratio);
- next step: create the Claude Project and upload the files.

## Mode: Update

Use this for a new document (report, plan, range, brand book page), a new decision, or a request to add a knowledge file.

1. Read `brain.json` and `00-README.md` first. Diff before editing. The owner may have hand-edited the files, and those edits stay.
2. Classify the new material: **source** (goes in the register), **decision** (settles an open item), **correction** (contradicts something basic: switch to Rebuild), or **new knowledge file**.
3. Update the source register: add the document with its status, and move anything it replaces to **Superseded** with "replaced by …". Business documents often supersede only part of an older one. Say which part.
4. Edit only the affected sections of the affected files. Use `scripts/apply_edits.py` for multi-file edits so each change is exact and reviewable. Close resolved open items (strike them or mark them **resolved <date>**, don't delete them silently). Add new conflicts as new numbered items.
5. If an agent team exists, run the relevant agents in parallel on the change, apply their JSON edits with `apply_edits.py` after reading them, and list their owner questions.
6. Add a dated changelog line to the README, then update `brain.json` `updated`.
7. Run the audit and rebuild the PDF (and the mind map if a leaf changed).

## Mode: Rebuild

Use this when the owner corrects the foundation (what the product is, who makes it, a name, the business model) or asks to redo the brain. Read `references/rebuild-protocol.md`. In short:

1. **Write the correction down first**, word for word, as a numbered entry in `brain.json` → `corrections` (`R1`, `R2`, `R2b`…), with the date and the rule. A later correction that refines an earlier one gets a letter (`R2b`) and says what it replaces. This log is permanent and survives every rebuild.
2. **Rebase the system file** on the correction.
3. **Re-derive every other file against it:** 01, 02, 03 and the knowledge files. Run them as parallel subagents where possible, each given the correction log plus the new system file. Add any newly banned phrase to `brain.json` → `banned_phrases`.
4. **Downstream documents:** grep the project for the old wording (business plan, research reports, context files, site copy) and list every hit. Don't rewrite those documents unless the user asks. Offer a dated update brief that states the correction and the rules, for whoever owns them.
5. **From scratch** (only when asked, or when the old brain is unsalvageable): move the old folder to `<out>/_archive/<YYYY-MM-DD>/`, run Build, and carry over the correction log, resolved decisions and the owner's hand edits that still hold.
6. Update the agents' shared "How you work" block if the core product facts changed. It repeats them by design.
7. Changelog line, audit, PDF.

## Mode: Audit

```bash
python3 <skill-dir>/scripts/brain_audit.py <brain-dir> [--strict]
```

It checks, using `brain.json`:
- every file in `read_order` exists and is listed in the README;
- every backticked path in the brain resolves (paths marked removed or outside the repo are skipped);
- banned phrases and never-print names don't appear, except in lines that ban them, and never-print names don't appear in the manifest's `public_paths` (the site, social copy);
- superseded sources aren't cited outside the register;
- open items are numbered without duplicates, and the changelog has an entry for `updated`.

Then do a read-through that the script can't: does every file agree with the system file and the correction log? Do prices and dates match the plan authority? Is anything PROPOSED presented as settled? Report the findings as one list, fix the mechanical ones, and ask about the rest.

## Image slots

When the brand has little real photography, add 2–3 image-generation briefs to the Brand kit's imagery section, each with an aspect ratio and a suggested file path. Write them as an art director's brief in plain prose: subject, setting, framing, light, materials, palette from the kit, and mood. Ground them in the brand's real place and materials. End each with "no text, no logos, no watermarks", and add "no people" unless the image needs them. Never name a never-print brand in a prompt. List them in the final reply.

## Notes

- **Confidentiality:** brains hold unreleased positioning, plans and benchmark names. Don't publish or push them anywhere unless the user asks.
- **Many brands:** one brain per brand, each in its own folder. Sub-brands get their own brain, with a line in the DNA and the system file pointing to the parent and saying what is shared (team, technology, factory) and what is not.
- **Scope:** the brain describes; it doesn't decide. When files disagree and no authority settles it, it's an open item for the owner, not a choice for Claude.
