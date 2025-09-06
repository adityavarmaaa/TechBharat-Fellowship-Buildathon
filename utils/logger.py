import logging
import os
from datetime import datetime
import json

LOG_DIR = os.environ.get('RTGS_LOG_DIR', 'outputs/logs')
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name='rtgs', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        fmt = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        fh = logging.FileHandler(os.path.join(LOG_DIR, f'{name}_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.log'))
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger

def write_audit(record: dict, filename='outputs/logs/audit.json'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, default=str) + '\n')
