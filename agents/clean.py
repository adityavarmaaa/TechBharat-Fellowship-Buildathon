"""Agent 2 — Clean & Transform
Dedupe, missing-value rules, unit normalization (to liters), location slugging, and flag suspicious records.
"""
import pandas as pd
import os
from slugify import slugify
from utils.logger import setup_logger, write_audit

logger = setup_logger('clean')

def normalize_volume_liters(df: pd.DataFrame):
    # Placeholder for unit heuristics
    return df

def run_clean(input_csv, outputs, thresholds):
    logger.info(f'Loading standardized CSV {input_csv}')
    df = pd.read_csv(input_csv)
    before = len(df)

    required = ['date', 'district', 'vehicle_id', 'volume']
    missing = [r for r in required if r not in df.columns]
    if missing:
        logger.warning(f'Missing required columns: {missing}')

    df = df.dropna(how='all')
    df = df.drop_duplicates()
    after_dedupe = len(df)

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

    if 'volume' in df.columns:
        df['volume'] = pd.to_numeric(df['volume'], errors='coerce')

    df['suspicious'] = False
    if 'volume' in df.columns:
        df['suspicious'] = df['volume'] > thresholds.get('suspicious_volume_liters', 100000)

    if 'district' in df.columns:
        df['district_slug'] = df['district'].fillna('unknown').apply(lambda x: slugify(str(x)))

    os.makedirs(outputs['tables'], exist_ok=True)
    out_path = os.path.join(outputs['tables'], 'cleaned.csv')
    df.to_csv(out_path, index=False)

    audit = {
        'stage': 'clean',
        'input': input_csv,
        'output': out_path,
        'rows_before': before,
        'rows_after_dedupe': after_dedupe,
        'rows_after': len(df)
    }
    write_audit(audit, filename=os.path.join(outputs['logs'], 'audit_clean.json'))
    logger.info('Clean complete; cleaned CSV written')
    return out_path

if __name__ == '__main__':
    import yaml
    cfg = yaml.safe_load(open('config/sample_config.yaml'))
    run_clean('outputs/tables/standardized.csv', cfg['outputs'], cfg['thresholds'])
