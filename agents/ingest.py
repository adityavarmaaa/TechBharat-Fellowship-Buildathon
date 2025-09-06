"""Agent 1 — Ingest & Standardize
Loads CSV, infers schema, applies canonical column names, writes standardized CSV.
"""
import pandas as pd
import os
from dateutil import parser
from utils.logger import setup_logger, write_audit

logger = setup_logger('ingest')

CANONICAL = {
    'date': ['date', 'service_date', 'dt'],
    'district': ['district', 'taluka', 'zone'],
    'vehicle_id': ['vehicle_id', 'truck_no', 'vehicle_no'],
    'source_point': ['from', 'source', 'src'],
    'dest_point': ['to', 'destination', 'dest'],
    'volume': ['volume', 'litres', 'liters', 'quantity']
}

def find_column(cols, candidates):
    for c in candidates:
        if c in cols:
            return c
    lower = {x.lower(): x for x in cols}
    for c in candidates:
        if c.lower() in lower:
            return lower[c.lower()]
    return None

def canonicalize_columns(df: pd.DataFrame):
    cols = df.columns.tolist()
    mapping = {}
    for canon, cands in CANONICAL.items():
        found = find_column(cols, cands)
        if found:
            mapping[found] = canon
    df = df.rename(columns=mapping)
    return df, mapping

def parse_date_safe(x):
    try:
        return parser.parse(str(x)).date()
    except Exception:
        return pd.NaT

def run_ingest(path, scope, outputs):
    logger.info(f'Loading {path}')
    df = pd.read_csv(path)
    orig_cols = df.columns.tolist()
    df, mapping = canonicalize_columns(df)
    logger.info(f'Canonical mapping applied: {mapping}')

    # parse date
    if 'date' in df.columns:
        df['date'] = df['date'].apply(parse_date_safe)

    # volume -> numeric
    if 'volume' in df.columns:
        df['volume'] = pd.to_numeric(df['volume'], errors='coerce')

    # basic scope filter
    if scope.get('district') and 'district' in df.columns:
        df = df[df['district'].str.contains(scope['district'], case=False, na=False)]
        logger.info(f'Scoped to district: {scope.get("district")} — {len(df)} rows remain')

    os.makedirs(outputs['tables'], exist_ok=True)
    out_path = os.path.join(outputs['tables'], 'standardized.csv')
    df.to_csv(out_path, index=False)
    audit = {
        'stage': 'ingest',
        'input_path': path,
        'output_path': out_path,
        'orig_columns': orig_cols,
        'mapping': mapping,
        'rows': len(df)
    }
    write_audit(audit, filename=os.path.join(outputs['logs'], 'audit_ingest.json'))
    logger.info('Ingest complete; standardized CSV written')
    return out_path

if __name__ == '__main__':
    import yaml, sys
    cfg = yaml.safe_load(open('config/sample_config.yaml'))
    run_ingest(cfg['dataset_path'], cfg['scope'], cfg['outputs'])
