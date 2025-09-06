#!/usr/bin/env python3
import argparse, yaml, os, sys
from agents import ingest, clean, analyze, docs_agent
from utils.logger import setup_logger

logger = setup_logger('cli')

def load_config(path):
    return yaml.safe_load(open(path))

def run_full(cfg_path):
    cfg = load_config(cfg_path)
    outputs = cfg['outputs']
    os.makedirs(outputs['base'], exist_ok=True)
    os.makedirs(outputs['tables'], exist_ok=True)
    os.makedirs(outputs['images'], exist_ok=True)
    os.makedirs(outputs['logs'], exist_ok=True)

    # Agent 1: ingest
    standardized = ingest.run_ingest(cfg['dataset_path'], cfg.get('scope', {}), outputs)

    # Agent 2: clean
    cleaned = clean.run_clean(standardized, outputs, cfg.get('thresholds', {}))

    # Agent 3: analyze
    insights = analyze.run_analysis(cleaned, outputs)

    # Agent 4: docs export
    manifest = docs_agent.export_manifest(cfg, outputs)

    print('\n=== RUN COMPLETE ===')
    print(f'Artifacts in: {outputs["base"]}')
    print(f'Insights file: {insights}')
    print(f'Manifest: {manifest}')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='RTGS CLI — one-shot run')
    p.add_argument('--one-shot', action='store_true', help='Run the full pipeline end-to-end')
    p.add_argument('--config', default='config/sample_config.yaml', help='Path to config YAML')
    args = p.parse_args()
    if args.one_shot:
        run_full(args.config)
    else:
        p.print_help()
