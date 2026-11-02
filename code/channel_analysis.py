"""Place C weekly analysis (Section 5.2 of the paper): channel prevalence (Tables 4 and 5), number of BSSIDs
(Table 6), distribution of the mean RSSI per BSSID for channels 36 and 149 (Figure 9) and the mean RSSI of
50 randomly selected BSSIDs repeated 100 times (Figure 10).

Usage: python channel_analysis.py        (run from the code/ folder; figures are written to ../results/)
"""
import glob, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from leafsense.preprocessing import prepare, timestamps_s, RSSI, BSSID, CH, LABEL

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DATA = os.path.join(ROOT, 'data')
RESULTS = os.path.join(ROOT, 'results'); os.makedirs(RESULTS, exist_ok=True)
WEEKS = {'Oct 1st': '10-01', 'Oct 30th': '10-30', 'Nov 8th': '11-08', 'Nov 14th': '11-14'}
CHANNELS = [1, 6, 11, 36, 40, 44, 48, 149, 153, 157, 161]
SELECTED = [36, 149]

weekly5 = pd.read_csv(os.path.join(DATA, 'processed/placeC_weekly/placeC_weekly_5ghz.csv.gz'), low_memory=False)
weekly24 = pd.read_csv(os.path.join(DATA, 'processed/placeC_weekly/placeC_weekly_2.4ghz.csv.gz'), low_memory=False)
oct_nov24 = pd.read_csv(os.path.join(DATA, 'processed/table2/placeC_2.4ghz_oct_nov.csv.gz'), low_memory=False)
oct1_24 = oct_nov24[oct_nov24[LABEL] == 'Leaves'].assign(**{LABEL: 'Oct 1st'})   # 1 Oct, 2.4 GHz
filtered = pd.concat([weekly5, weekly24, oct1_24], ignore_index=True)

# ---- Tables 4 and 5: share of seconds in which at least one sample was received on a channel ----
print('Table 4 - prevalence of each channel (%)')
print(f'{"":10s}' + ''.join(f'{"Ch " + str(c):>8s}' for c in CHANNELS) + f'{"36&149":>9s}')
for week, date in WEEKS.items():
    files = glob.glob(os.path.join(DATA, 'raw', f'placeC_{date}', '*.csv.gz'))
    raw = prepare(pd.concat([pd.read_csv(f, low_memory=False) for f in files], ignore_index=True))
    raw['_s'] = np.floor(timestamps_s(raw['frame.time']))
    total = raw['_s'].nunique()
    row = [100 * raw.loc[raw[CH] == c, '_s'].nunique() / total for c in CHANNELS]
    both = 100 * raw.loc[raw[CH].isin(SELECTED), '_s'].nunique() / total
    print(f'{week:10s}' + ''.join(f'{v:8.2f}' for v in row) + f'{both:9.2f}')

# ---- Table 6: number of BSSIDs ----
print('\nTable 6 - number of BSSIDs')
for week in WEEKS:
    w = filtered[filtered[LABEL] == week]
    print(f'{week:10s} channels 36 and 149: {w.loc[w[CH].isin(SELECTED), BSSID].nunique():4d}   all channels: {w[BSSID].nunique():4d}')

# ---- Figure 9: mean RSSI per BSSID, channels 36 and 149 ----
sel = weekly5[weekly5[CH].isin(SELECTED) & weekly5[LABEL].isin(WEEKS)]
per_ap = sel.groupby([LABEL, BSSID])[RSSI].mean().reset_index()
boxes = [per_ap.loc[per_ap[LABEL] == w, RSSI].values for w in WEEKS]
print('\nFigure 9 - overall mean of the per-BSSID mean RSSI (dBm): ' +
      ', '.join(f'{w}: {np.mean(b):.2f}' for w, b in zip(WEEKS, boxes)))
plt.figure(figsize=(8, 5))
plt.boxplot(boxes, showmeans=True, meanline=True); plt.xticks(range(1, len(WEEKS) + 1), list(WEEKS))
for i, b in enumerate(boxes):
    plt.text(i + 1, np.mean(b), f'{np.mean(b):.2f}', ha='center', va='bottom', color='blue')
plt.xlabel('Week'); plt.ylabel('RSSI (dBm)'); plt.grid(True)
plt.savefig(os.path.join(RESULTS, 'figure9_mean_rssi_per_bssid.png'), dpi=200, bbox_inches='tight'); plt.close()

# ---- Figure 10: 50 randomly selected BSSIDs per week, repeated 100 times ----
rng = np.random.default_rng(0)
runs = []
for _ in range(100):
    means = {}
    for w in WEEKS:
        g = sel[sel[LABEL] == w]
        aps = g[BSSID].unique()
        pick = rng.choice(aps, min(50, len(aps)), replace=False)
        means[w] = g[g[BSSID].isin(pick)][RSSI].mean()
    runs.append(means)
runs = pd.DataFrame(runs)
print('Figure 10 - median over 100 repetitions (dBm): ' + ', '.join(f'{w}: {runs[w].median():.2f}' for w in WEEKS))
plt.figure(figsize=(8, 5))
plt.boxplot([runs[w] for w in WEEKS]); plt.xticks(range(1, len(WEEKS) + 1), list(WEEKS))
plt.xlabel('Week'); plt.ylabel('Mean RSSI (dBm)'); plt.grid(True)
plt.savefig(os.path.join(RESULTS, 'figure10_random_50_bssids.png'), dpi=200, bbox_inches='tight'); plt.close()
