# GCC Door Project Intelligence & Qualification System

Internal business-intelligence tool for **SBK** (imports doors from China, sells
across the GCC). It finds construction projects early, **qualifies them hard**,
and surfaces only the serious ones — so the team enters funded projects *before*
the door specification is locked.

> Internal tool. Not an e-commerce site, marketplace, or tendering platform.
> Run it locally / behind the team network.

---

## Data-sourcing rules (built into the architecture)

1. **Never scrape or crawl paid subscription platforms** (MEED, ProTenders,
   Ventures ONSITE, BNC, GlobalData). Their data enters **only** via official
   **export files** (file-import connector) or **official API access** (API
   connector — later phase), using credentials *you* supply.
2. **Public government portals** (Saudi Etimad, Qatar Ashghal, etc.) may be
   monitored directly **only where terms permit** — the portal-monitor connector
   checks `robots.txt` and honors rate limits, preferring official RSS/API/open
   data. (Implemented as a guarded scaffold; per-portal parsing is a later phase.)
3. **Pluggable connectors** — add a source by dropping in an export file, an API
   credential, or a portal config; the core never changes.
4. **Credentials live in `.env`** (see `.env.example`). Nothing hardcoded or
   committed.

## Geographic scope

Full GCC — Saudi Arabia, UAE, Qatar, Bahrain, Oman, Kuwait — with **Iraq** as a
toggleable region (`regions.include_iraq` in `config/config.yaml`). `country` is
a first-class, weighted field.

---

## Architecture

```
config/config.yaml          All weights / thresholds / heuristics (no magic numbers)
config/mappings/*.yaml       Per-source column-mapping profiles (meed, protenders, etimad, generic)
app/connectors/              file_import (Phase 1) · api_connector + portal_monitor (scaffolds)
app/normalization/           vocab (controlled vocabularies) · normalize · dedupe (fuzzy+merge) · enrich
app/scoring/scorecard.py     Weighted 0–100 score → tier A/B/C + full breakdown
app/alerts/                  console / email(SMTP) / webhook channels + digest
app/pipeline.py              ingest → staging(raw copy) → normalize → dedupe → enrich → score → alert
app/main.py + app/web/       FastAPI UI: pipeline board, project detail, map, KPIs, manual add, upload
data/samples/                Sample MEED/ProTenders/Etimad exports (incl. a cross-source duplicate)
scripts/seed.py              Load samples through the whole pipeline (no credentials needed)
scripts/run_ingest.py        CLI: ingest a file / send a digest
tests/                       End-to-end Phase-1 tests
```

The ingestion flow keeps a **raw copy of every record** (`staging_records`) for
traceability, merges duplicates across sources into one `Project` (preserving all
`source_refs`), then enriches and scores.

## Qualification scorecard (the core)

Score 0–100 from six configurable weighted factors (defaults in `config.yaml`):

| Factor | Default weight | Notes |
|---|---|---|
| Funding / status | 30 | awarded/under-construction high; on-hold/cancelled = **auto-disqualify** |
| Spec-influence window | 25 | design/pre-tender high (spec not yet locked) |
| Door relevance | 20 | from `estimated_door_demand` vs a configurable floor |
| Fire-rating need | 10 | bonus (highest-margin zone) |
| Reachability | 10 | named, contactable stakeholder present |
| Country weighting | 5 | Saudi & Qatar highest by default |

Tiers: **A ≥ 70 (pursue now)**, **B ≥ 45 (watch)**, **C (auto-archive)**. The
per-factor `score_breakdown` is stored and shown in the UI so the team sees *why*.

---

## Quick start

```bash
cd gcc-door-intel
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # optional: only needed for email/webhook alerts

# 1) Load sample data through the full pipeline (no credentials required)
python -m scripts.seed

# 2) Run the dashboard
uvicorn app.main:app --reload --port 8000
# open http://localhost:8000
```

### Ingest your own export file

```bash
python -m scripts.run_ingest --file /path/to/MEED_export.xlsx --profile meed
```

Or use the **Import file** page in the UI. To add a new source, copy
`config/mappings/generic.yaml`, point the left-hand keys at your file's column
headers, and select it on upload.

### Alerts

Channels are set in `config.yaml` (`alerts.channels`): `console` (default),
`email`, `webhook`. Email/webhook read secrets from `.env`. On each ingestion run
new **Tier-A** projects and **spec-window-opening** status changes are pushed.
Send a digest with `python -m scripts.run_ingest --digest`.

### Tests

```bash
python -m pytest -q
```

---

## Roadmap

- **Phase 1 (done):** file-import connector, unified schema + raw staging,
  normalize/dedupe/enrich, scorecard, alerts, dashboard, sample data, tests.
- **Phase 2:** official API connectors (e.g. enterprise MEED feed).
- **Phase 3:** public-portal monitors (Etimad/Ashghal/etc.) — robots/rate-limit aware.
- **Phase 4:** richer enrichment heuristics, extra alert channels, auth for the UI.
