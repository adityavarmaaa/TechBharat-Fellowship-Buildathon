**  Video Explanation :**     https://www.loom.com/share/8b5cecee0c8e46b8a53d3fb79d8059e0?sid=577cee86-3c6f-4e84-9c90-2e42e7a86ce2    Continued: https://www.loom.com/share/6775a99611f74c58a77a6bfb1ce7c737?sid=ee3fa3ca-ffab-4308-abf3-966e48e4fc6f
                  

# RTGS-Style AI Analyst — Telangana Open Data (HMWSSB Water Tankers, Jan 2022)

**Quick:** This repo is a CLI-first, agentic pipeline that ingests the HMWSSB water tanker dataset (Jan 2022), cleans it, analyzes it, and writes terminal-friendly outputs plus saved artifacts. Scope by default: **Hyderabad district** (change `config/sample_config.yaml`).

## One-shot run (after placing your dataset)
1. Put `hmwssb_water_tankers_jan2022.csv` inside `data/`.
2. Create and activate a Python venv, then install deps:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run full pipeline (one-shot):
   ```bash
   python cli.py --one-shot --config config/sample_config.yaml
   ```

Outputs will be in `outputs/` (tables, logs, images). See `outputs/logs` for audit trail JSON lines showing each agent's actions.

## Repo layout
```
rtgs-telangana-hmwssb/
├── README.md
├── requirements.txt
├── run.sh
├── config/
│   └── sample_config.yaml
├── data/
│   └── hmwssb_water_tankers_jan2022.csv  # (place your CSV here)
├── outputs/
│   ├── logs/
│   ├── tables/
│   └── images/
├── agents/
│   ├── ingest.py
│   ├── clean.py
│   ├── analyze.py
│   └── docs_agent.py
├── cli.py
├── utils/
│   └── logger.py
├── manifests/
│   └── dataset_manifest.yaml
└── demo_video_link.txt
```

## Implementation notes
- Agentic workflow: ingest -> clean -> analyze -> docs/logs -> CLI formatting.
- Agents communicate through CSV/JSON files in `outputs/` to keep work auditable.
- All transforms are logged to `outputs/logs/*.json` as newline-delimited JSON audit records.
- CLI is intentionally simple and terminal-first (prints ASCII tables via `tabulate` and saves PNG charts).

## Demo video
Place unlisted link in `demo_video_link.txt` after recording and top of README.md.

