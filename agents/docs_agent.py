"""Agent 4 — Documentation & Logging agent
Generates manifest export and readable changelog describing transformations.
"""
import os, yaml, json
from utils.logger import setup_logger, write_audit
logger = setup_logger('docs')

def export_manifest(cfg, outputs):
    manifest = {
        'dataset': cfg.get('dataset_path'),
        'scope': cfg.get('scope'),
        'outputs': outputs
    }
    os.makedirs(outputs['tables'], exist_ok=True)
    out = os.path.join(outputs['tables'], 'dataset_manifest_export.yaml')
    with open(out, 'w', encoding='utf-8') as f:
        yaml.safe_dump(manifest, f)
    write_audit({'stage': 'docs', 'manifest_exported': out}, filename=os.path.join(outputs['logs'], 'audit_docs.json'))
    logger.info(f'Manifest exported to {out}')
    return out

if __name__ == '__main__':
    import yaml
    cfg = yaml.safe_load(open('config/sample_config.yaml'))
    export_manifest(cfg, cfg['outputs'])
