# Rebuild protocol: owner corrections and rebasing

An owner correction is different from a new document. It says the brain's idea of the product was wrong, so every file built on that idea is now suspect. Partial patching leaves contradictions behind, so rebase instead.

## 1. Record the correction

Add it to `brain.json` → `corrections` before touching any file:

```json
{"id": "R2", "date": "2026-10-15",
 "rule": "The frame is the brand's own (same team as the sister company); never treat it as a supplier. No transfer prices or margins between them.",
 "replaces": "R1 wording 'sister company supplies the frame'",
 "banned_phrases_added": ["transfer price", "group view"]}
```

- Quote the owner's words where you can. Don't soften them.
- A later correction that refines an earlier one gets a letter (`R2b`) and states what it replaces. Example: the owner first says "call it the X shell", then says "never say shell". Keep both entries. The later one wins, and the old wording becomes a banned phrase.
- Add every newly banned wording to `brain.json` → `banned_phrases`, so the audit catches it from now on.

## 2. Rebase order

1. **System file:** rewrite sections 1–6 on the correction. Keep the build-up and conflicts that still hold.
2. **03 Brand DNA:** six lines, how we solve it, why we're different, proof. These usually change most.
3. **02 Voice rules:** locked lines, banned words, truth rules.
4. **01 Brand kit:** usually only imagery and do/don't change.
5. **Knowledge files:** check every reference to the corrected fact.
6. **README:** the project instructions block (it repeats the core facts), starter prompts, open items, changelog.
7. **Agents:** the shared "How you work" block repeats the core facts. Update every agent file.

Run 2–5 as parallel subagents, each given: the correction log, the new system file, its own file and the ground rules. Ask for JSON edits (see `agent-team.md`) and apply them with `scripts/apply_edits.py` after reading them.

## 3. Downstream documents

The correction usually also invalidates the business plan, research reports, a context file, site copy or social copy. Grep for the old wording and list every hit with its path:

```bash
grep -rniE "old phrase|other old phrase" <root> --include=*.md --include=*.html --include=*.tsx -l
```

Don't rewrite those documents inside a brain rebuild unless the user asks, because they have their own owners and build steps. Offer to write a dated **update brief** next to them that states the correction, numbered rules for every update, what to keep (sourced research), and how to re-render. Owners or agents can then apply it.

## 4. From-scratch rebuild

Only when asked, or when the old brain is unsalvageable:
1. Move the old brain to `<out>/_archive/<YYYY-MM-DD>/` (don't delete it).
2. Run Build mode in full.
3. Carry over: the correction log, resolved decisions (as settled facts), the owner's hand edits that still hold (diff the archive), and the open items that are still open (keep their numbers).
4. Changelog: "Rebuilt from scratch <date>; previous version in `_archive/<date>/`."
