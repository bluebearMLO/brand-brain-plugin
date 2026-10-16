# mindmap.json schema (input to scripts/mindmap.py)

```json
{
  "title": "Acme Brand Brain",
  "root_title": "Acme",
  "tagline": "Brand line here.",
  "background": "#f2eee7",
  "root_color": "#1c1d1b",
  "root_text": "#f2eee7",
  "branches": [
    {"name": "1  Project",   "color": "#5c5e4d", "leaves": ["Claude Project: Acme Brand Brain", "Custom instructions", "Source register"]},
    {"name": "System",       "color": "#3d4a3e", "leaves": ["Product: part A + part B + part C", "Who does what", "May / never say"]},
    {"name": "2  Brand kit", "color": "#67422b", "leaves": ["Logo: ...", "Palette: ...", "Type: ...", "Imagery: ..."]},
    {"name": "3  Voice rules","color": "#9fb3ba", "leaves": ["We are: ...", "Locked lines: ...", "Never: ..."]},
    {"name": "4  Brand DNA", "color": "#a7a096", "leaves": ["Who: ...", "Problem: ...", "Solve: ...", "Different: ...", "Proof: ..."]},
    {"name": "Knowledge",    "color": "#6f6a5f", "leaves": ["Design standards", "Design benchmark (never named)"]},
    {"name": "5  Create",    "color": "#1c1d1b", "leaves": ["Social posts", "Website pages", "Emails", "Image briefs", "Copy review"]}
  ]
}
```

`root_title` is optional (it defaults to `title`) and wraps automatically, but a short brand name reads best. Keep leaves under about 110 characters (3 wrapped lines at most). Branch text colour is picked automatically for contrast. Any number of branches works; drop Knowledge if the brain has no 05+ files.
