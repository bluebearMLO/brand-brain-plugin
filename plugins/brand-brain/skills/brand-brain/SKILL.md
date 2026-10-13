---
name: brand-brain
description: Build a "Brand Brain" for a company, brand or project, meaning the three knowledge files (Brand kit, Voice rules, Brand DNA) that go into a Claude Project so every chat produces on-brand work. Also produces a setup guide, a mind map and a PDF. Use this whenever someone wants to capture a brand for Claude, make Claude write or design "on brand", set up a brand Claude Project, distil brand guidelines, voice/tone rules or positioning from existing files, or says things like "make the brain for X", "brand brain", "do the brand setup for this client", even if they don't name the skill. It works from a folder of brand material, a website, or an interview when nothing exists yet.
---

# Brand Brain

A Brand Brain is a Claude Project holding three knowledge files:

| File | Answers |
|---|---|
| `01-brand-kit.md` | What it looks like: logo, colours (hex), type, UI, imagery, do/don't |
| `02-voice-rules.md` | How it sounds: traits, set phrases, banned words, formatting, what may be claimed |
| `03-brand-dna.md` | Who it's for and why it wins: customer, problem, solution, difference, proof |

Every chat started in that project then has the brand loaded. This skill builds those files from whatever the brand already has, and asks the owner for anything it can't find. Getting the facts right matters more than polish: a Brand Brain that invents a statistic or a price will repeat it in every ad it writes.

## The five steps (the method behind the files)

1. **Project.** Create a Claude Project named "<Brand> Brand Brain".
2. **Brand kit.** Upload the existing logo, colours and fonts. If there are none, run the design-system interview (see below).
3. **Voice.** Upload everything the brand has written, then distil it into voice rules.
4. **Brand DNA.** Fill in the 6-line positioning template.
5. **Create.** Open chats inside the project and ask for ads, pages, posts and emails.

Steps 2–4 are this skill's job. Steps 1 and 5 are for the user; the setup guide tells them how.

## Workflow

### 0. Scope the job

Work out three things, and ask only if they aren't clear from the request:
- **Target:** a local folder (best), a website URL, uploaded files, or nothing (interview mode).
- **Brand name.**
- **Output folder:** suggest `<target>/brand-brain/` (or `./brand-brain-<slug>/` with no folder) and confirm it, because writing into a client's repo can break that repo's own rules (check its `CLAUDE.md`/`AGENTS.md`). Never write into the user's Desktop root.

### 1. Inventory the sources

Look for brand material and rank it by authority before reading deeply. Useful places:
- Brand guidelines, brand books, production decks (PDF/PPTX). These are usually the **identity authority**.
- `positioning.md`, `PRODUCT.md`, `DESIGN.md`, `README`, `CLAUDE.md`/`AGENTS.md`, plans and roadmaps.
- Design tokens: `globals.css`, `tailwind.config`, theme files, Figma exports, logo SVGs.
- Written copy: site pages and components, blog/journal posts, emails, newsletters, social captions, bios.
- Market material: competitor reports, research notes, pitch decks.

Skip `node_modules`, `.next`, `dist`, `.git`, `.venv` and lock files. With a website target, scrape the home, about, product and blog pages with whatever fetch or scrape tool is available.

Then decide two **authorities** and write them down:
- **Identity authority**, which decides on logo, colour and type. Use the brand book or deck. With no brand book, use the most deliberate design document (a design-system file, a style guide). As a last resort use the shipped tokens, and say so.
- **Claims authority**, which decides what may be stated as fact. Use the most formal published document: a capability statement, product spec, `PRODUCT.md` or the plans.

When **shipped code disagrees with the design docs** (a different font loaded, a colour used differently), record both. The docs show what the brand intends and the code shows what is live. Mark the item **owner call** instead of picking one, so all three files treat it the same way.

**Pre-read before delegating.** Skim the key sources yourself first. Extract big PDFs or decks once to text files in a scratch folder and pass those paths on, so each subagent doesn't re-extract them. Note the key facts and any conflicts you've already spotted. The ranked list, the two authorities, the key facts and the known conflicts go into every subagent brief, and the ranked list becomes the "Source keys" block at the top of each file.

### 2. Build the three files (in parallel if you can)

If an Agent/subagent tool is available, start three subagents in one message, one per file, so they run at the same time. Give each one:
- the brand name, the project root and the output path;
- the ranked source list (with paths to pre-extracted text), the two authorities, key facts and known conflicts;
- its template from `references/`, which it should read first (`brand-kit-template.md`, `voice-rules-template.md` or `brand-dna-template.md`);
- the ground rules below, copied word for word.

Without subagents, do the three files one after another yourself.

**Ground rules (put these in every subagent prompt):**
- Extract; don't invent. Every hex code, font, tagline, number and claim must come from a source. Add a short `Source:` line or `[KEY]` tag to each section.
- When sources disagree, the identity authority wins on look and the claims authority wins on facts. Record every conflict in the file's "Source conflicts" table rather than silently picking one. Code-vs-docs disagreements are **owner call**.
- Give each rule a status where it's in doubt: **followed** (the existing copy does it), **wish** (stated but not followed), or **owner call** (undecided).
- Names that must never appear in public (a supplier, a machine brand, a client under NDA) can be named inside the knowledge files, so Claude knows what to avoid. Put them in a clearly headed "Never print" list.
- Put hex codes and font names in plain text, not only in images, so Claude can reuse them.
- Proof is only what can be verified. Give "proof we don't have yet / do not claim" its own list: prices, dimensions, client names, reviews, stats or awards that aren't in the sources.
- Quote real lines verbatim, with their file path, as gold-standard examples.
- Keep each file dense and scannable: 120–300 lines of tables and short bullets.
- Only write your own file.

### 3. Fill gaps by interview (only what's missing)

- **No visual identity:** use the design-system prompt in `references/interview-prompts.md`. It asks 5 questions first, then proposes a logo direction, a palette with hex codes, fonts, buttons/cards/spacing and do/don't rules. Mark everything it produces as **proposed** until the owner approves it.
- **No written copy:** use the voice interview in the same file.
- **No positioning:** go through the 6 Brand DNA lines with the owner one at a time.

Ask questions in one batch rather than one by one. If the user wants a first draft now, write clearly labelled `[TO CONFIRM]` placeholders instead of guessing.

### 4. Write the setup guide `00-README.md`

Use `references/readme-template.md`. It must include:
- the three files and what each gives Claude;
- step-by-step Claude Project setup, including which logo and asset files to upload alongside;
- **project custom instructions** ready to paste (brand one-liner, "follow the files", spelling convention, truth rules, "ask if a fact isn't in the files");
- 5–6 starter prompts suited to this brand's channels;
- **open items to confirm**: every conflict and gap the subagents reported, numbered, so the owner can fix the source of truth.

### 5. Mind map

Write a `mindmap.json` (schema in `references/mindmap-schema.md`): the brand at the root, then 5 branches (Project, Brand kit, Voice rules, Brand DNA, Create) with 3–5 short leaves each, all taken from the files you just wrote. Use the brand's own colours. Then run:

```bash
python3 <skill-dir>/scripts/mindmap.py <out>/mindmap.json <out>/<Brand>-Brand-Brain-mindmap.svg
```

Open or render the SVG and check it: no text should be clipped and no branch should be empty. Keep leaves short and set `root_title` to just the brand name if it's long.

**Miro (optional):** if Miro tools are connected and the user wants a board, build the same tree there. Use `canvas_get_canvas_composer_skill` and then the `free_form` diagramming guidance: a root on the left, branches, leaves on the right, elbowed connectors, and branch colours from the palette. Creating a board is visible to others in the user's Miro team, so confirm before creating it unless they already asked for Miro.

### 6. PDF

```bash
python3 <skill-dir>/scripts/build_pdf.py <out> --title "<Brand> Brand Brain" --tagline "<brand line>" --primary "#hex" --accent "#hex" --paper "#hex"
```

This combines the mind map, `00-README.md` and the three files (one section per page) into `<out>/<Brand>-Brand-Brain.pdf` through headless Chrome or Chromium. If no browser is found, it prints the HTML path; tell the user to open it and use Print → Save as PDF. Afterwards, render a page or two (`pdftoppm` if available) and look at them before saying the PDF is done.

### 7. Report back

Keep the reply short:
- the output folder and a table of the files;
- the 6-line Brand DNA, which is the quickest check that you understood the brand;
- the most important open items and conflicts;
- the user's next step: create the Claude Project and upload the files.

### Image slots

When the brand has little real photography, add 2–3 image-generation briefs to the Brand kit's imagery section, each with an aspect ratio and a suggested file path. Write them as an art director's brief in plain prose: subject, setting, framing, light, materials, palette from the kit, and mood. End each with "no text, no logos, no watermarks". List them in your final reply so the owner knows what to generate.

## Notes

- **Confidentiality:** these files often contain unreleased positioning, so don't publish or push them anywhere unless the user asks.
- **Re-runs:** when a `brand-brain/` folder already exists, update it in place and add a dated changelog line to `00-README.md` instead of overwriting the owner's edits blindly. Diff first.
- **Many brands:** run once per brand with separate output folders. Sub-brands get their own Brand Brain, with a line in the DNA pointing to the parent brand.
