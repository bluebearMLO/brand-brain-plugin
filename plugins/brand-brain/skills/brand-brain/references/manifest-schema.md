# `brain.json` manifest

Sits in the brain folder. The README is for people; `brain.json` is for the audit script, for rebuilds and for agents. Keep the two in agreement. All paths are relative to `project_root`, which is itself relative to the brain folder (or absolute).

```json
{
  "brand": "Acme",
  "slug": "acme",
  "project_root": "../../..",
  "built": "2026-10-13",
  "updated": "2026-10-15",
  "read_order": [
    "04-the-acme-system.md",
    "01-brand-kit.md",
    "02-voice-rules.md",
    "03-brand-dna.md",
    "05-acme-design-standards.md"
  ],
  "authorities": {
    "identity": "docs/brand/brand-book.pdf",
    "claims": "PRODUCT.md",
    "plan": "docs/business-plan/Acme-Business-Plan.pdf",
    "calendar": "docs/business-plan/ROADMAP.md"
  },
  "sources": {
    "current": [
      {"path": "docs/business-plan/ROADMAP.md", "what": "Launch roadmap", "status": "current"},
      {"path": "docs/business-plan/FINANCIALS.md", "what": "Plan numbers", "status": "current, only the CURRENT NUMBERS section"},
      {"path": "docs/range/Acme-Range-2027.md", "what": "Model range", "status": "proposed", "internal": true}
    ],
    "superseded": [
      {"path": "docs/business-plan/PLAN-BRIEF.md", "replaced_by": "docs/business-plan/ROADMAP.md", "note": "calendar only; writer rules still apply"}
    ],
    "not_sources": ["docs/business/BRIEF.md"]
  },
  "never_print": ["BenchmarkCo", "MachineMaker"],
  "banned_phrases": ["world-class", "fireproof", "official partner"],
  "locked_lines": ["Built to last a lifetime."],
  "public_paths": ["web/app", "social"],
  "corrections": [
    {"id": "R1", "date": "2026-10-14", "rule": "…", "replaces": null, "banned_phrases_added": []}
  ],
  "agents": [".claude/agents/acme-brand-guardian.md"]
}
```

| Field | Used by |
|---|---|
| `read_order` | PDF order, README files table, audit "file exists and is listed" |
| `authorities` | subagent briefs; audit checks the paths exist |
| `sources.current` / `superseded` / `not_sources` | README register; audit flags superseded or not-source paths cited outside the register |
| `never_print`, `banned_phrases` | audit scans the brain (lines that ban them are allowed) and `public_paths` (`never_print` only, no exceptions) |
| `locked_lines` | voice rules; audit warns if a locked line is missing from `02-voice-rules.md` |
| `corrections` | rebuilds; every subagent brief; agents' shared block |
| `agents` | rebuilds update their shared block; audit checks they exist |
