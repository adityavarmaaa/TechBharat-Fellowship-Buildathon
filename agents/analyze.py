"""Agent 3 — Analyze & Insight Generation
Compute KPIs and generate terminal-friendly artifacts and saved PNG charts.
"""
import pandas as pd
import os
from tabulate import tabulate
import matplotlib.pyplot as plt
from utils.logger import setup_logger, write_audit

logger = setup_logger('analyze')

def compute_kpis(df: pd.DataFrame):
    kpis = {}
    if 'date' in df.columns:
        daily = df.groupby('date').agg({'volume': 'sum', 'vehicle_id': 'nunique'}).reset_index()
        kpis['daily_totals'] = daily
    if 'district' in df.columns:
        by_district = df.groupby('district').agg({'volume': 'sum', 'vehicle_id': 'nunique'}).reset_index()
        kpis['by_district'] = by_district
    if 'vehicle_id' in df.columns:
        topv = df.groupby('vehicle_id').agg({'volume': 'sum'}).sort_values('volume', ascending=False).head(10)
        kpis['top_vehicles'] = topv
    return kpis

def save_volume_trend(df_daily, out_png):
    plt.figure()
    plt.plot(df_daily['date'], df_daily['volume'])
    plt.title('Daily volume (liters) — scoped')
    plt.xlabel('Date')
    plt.ylabel('Volume (L)')
    plt.tight_layout()
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.savefig(out_png)
    plt.close()

def run_analysis(clean_csv, outputs):
    logger.info(f'Loading cleaned CSV {clean_csv}')
    df = pd.read_csv(clean_csv)
    kpis = compute_kpis(df)

    if 'by_district' in kpis:
        table = kpis['by_district']
        print('\n=== Volume by District ===')
        print(tabulate(table, headers='keys', tablefmt='github', showindex=False))
        table.to_csv(os.path.join(outputs['tables'], 'by_district.csv'), index=False)

    if 'daily_totals' in kpis:
        daily = kpis['daily_totals']
        print('\n=== Daily Totals (first 10 rows) ===')
        print(tabulate(daily.head(10), headers='keys', tablefmt='psql', showindex=False))
        daily.to_csv(os.path.join(outputs['tables'], 'daily_totals.csv'), index=False)
        png = os.path.join(outputs['images'], 'volume_trend.png')
        save_volume_trend(daily, png)
        logger.info(f'Volume trend chart written to {png}')

    insights = []
    if 'daily_totals' in kpis:
        tot = int(daily['volume'].sum())
        maxd = daily.loc[daily['volume'].idxmax()]['date']
        insights.append(f'Total supplied volume (scoped): {tot} liters')
        insights.append(f'Day with maximum supply: {maxd}')

    insights_md = '# Insights\n' + '\n'.join(['- ' + s for s in insights])
    os.makedirs(outputs['tables'], exist_ok=True)
    with open(os.path.join(outputs['tables'], 'insights.md'), 'w', encoding='utf-8') as f:
        f.write(insights_md)

    audit = {
        'stage': 'analyze',
        'rows': len(df),
        'insights_count': len(insights)
    }
    write_audit(audit, filename=os.path.join(outputs['logs'], 'audit_analyze.json'))
    logger.info('Analysis complete; insights and visuals generated')
    return os.path.join(outputs['tables'], 'insights.md')

if __name__ == '__main__':
    import yaml
    cfg = yaml.safe_load(open('config/sample_config.yaml'))
    run_analysis('outputs/tables/cleaned.csv', cfg['outputs'])
