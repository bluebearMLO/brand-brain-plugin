# Project agent team

A brain goes stale as soon as the plan moves. A few project-level subagents, each with one lens, let the owner say "run the team on the new plan" and get precise, reviewable edits back. They live in `<root>/.claude/agents/<slug>-<role>.md`.

## Roles

| Agent | Lens | Edits (via JSON) | Reads |
|---|---|---|---|
| `<slug>-brand-guardian` | voice, claims, names, visual rules, image prompts, never-print, README source register | 00, 01, 02, 03 | everything |
| `<slug>-business-analyst` | brain matches the plan: dates, prices, money (Estimates), range vs price list | system file "plan" section, README register, context file | plan, roadmap, financials (current part only), research index |
| `<slug>-buyer-advocate` | the range and the copy as each buyer segment in 03 would see them: fit, budget, gaps, confusing names | range document only, where a need is clearly unmet; otherwise reports | customer and market research |
| `<slug>-<domain-expert>` ×1–2 | can it be made, does it work, is it safe and legal | system file build-up, technical standards, range | technical and regulatory research |

Derive the domain experts from the system file's "Who does what" and "How it's made" sections. Examples:
- a sauna on a steel frame: a sauna architect and a steel/building engineer;
- skincare: a formulation chemist and a regulatory reviewer;
- a SaaS product: a solutions architect and a security reviewer;
- food: a food technologist and a labelling reviewer.

Give experts relevant installed skills in their frontmatter (`skills:`) when the harness has them.

## Agent file template

```markdown
---
name: <slug>-<role>
description: <Brand> <role>. <One sentence on the lens and what it keeps consistent.>
tools: Read, Grep, Glob, Bash, Skill, WebSearch, WebFetch
---

You are the <Brand> <role>. Your lens: <3–5 concrete questions this agent asks>.
Sources (read only): <paths>. Your files to edit: <paths>.

## How you work (all <Brand> agents)
<the shared block below, identical in every agent>
```

## The shared "How you work" block

It repeats the core product facts on purpose, so an agent working alone can't drift. Update it in every agent file on any rebuild.

```markdown
- Root: <absolute project root>. Read <brain>/<system file> first, then 00-README.md and the files your role needs.
- <Brand> = <the product in one line, from the system file>. <The 1–3 owner corrections most likely to be broken.>
- <Writing rules: plain language, banned phrases, never-print names, "built with" partner rule, money = Estimates.>
- You do NOT edit files. Return your edits as a JSON array:
  [{"file": "<path>", "old": "<exact existing text>", "new": "<replacement>", "why": "<one line>"}].
  To add a section, use a heading line as "old" and put that heading plus the new text in "new".
  "old" must match the file exactly and be unique in it.
- Mark anything not already settled in the brain as PROPOSED (owner to approve) in the text itself.
- After the JSON, list in at most 10 lines: conflicts you found, and questions only the owner can answer.
```

## Running the team

1. Start the relevant agents in one message so they run in parallel, each with the change in question (new plan, new range, correction).
2. Save each agent's JSON to a scratch file. Read it, drop edits that overstep the agent's files or present PROPOSED items as settled, and resolve overlaps (two agents editing the same line: keep the one from the file's owner).
3. Dry-run first, then apply:
   ```bash
   python3 <skill-dir>/scripts/apply_edits.py edits.json --root <project-root>          # dry run
   python3 <skill-dir>/scripts/apply_edits.py edits.json --root <project-root> --apply
   ```
4. Collect the owner questions into the README's open items, numbered and dated.
5. Audit and rebuild the PDF.
