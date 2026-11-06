# Cupertino2
## Inheritance decision dashboard

Static GitHub Pages site in `docs/` (served from `main` `/docs`). It compares live, rent, and sell options for two properties inherited through a trust (anonymized: Property A = Cupertino, CA; Property B = San Francisco, CA; no names, addresses, or ZIP codes).

- `data/sources.json`: registry of every source (official or secondary) with its URL.
- `data/facts.json`: fact register; each row has a status (verified, partially verified, user-provided, secondary, assumption) and source IDs.
- `data/property_history.json`, `data/flagged.json`: owner-provided values (unverified) and the Flagged for Review list.
- `scripts/model.py`: projection and net-worth model (writes `data/projections_base.csv`, `data/sensitivity.csv`, `data/decision.json`).
- `scripts/build_site.py`: builds `docs/` and fails if any row lacks a registered source or any link is broken.

Rebuild:

```
python3 scripts/model.py && python3 scripts/build_site.py
```

This is research, not legal or tax advice. See `COORDINATION.md` for the task board and the flagged items.
