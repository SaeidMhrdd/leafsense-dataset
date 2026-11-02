"""Robustness to the vehicle's path (Figure 11) and access-point density (Figure 12), Section 5.4 of the paper.

Usage: python path_and_density.py        (run from the code/ folder; figures are written to ../results/)
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from leafsense.preprocessing import timestamps_s, BSSID, LABEL

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DATA = os.path.join(ROOT, 'data', 'processed')
RESULTS = os.path.join(ROOT, 'results'); os.makedirs(RESULTS, exist_ok=True)

# ---- Figure 11: five runs at Place C (4 April), 100 random BSSIDs per run, 100 repetitions ----
runs = pd.read_csv(os.path.join(DATA, 'fig11_path_robustness/placeC_04-04_five_runs.csv.gz'), low_memory=False)
names = sorted(runs[LABEL].unique())                       # split-1 ... split-5
print('Figure 11 - unique BSSIDs per run: ' + ', '.join(f'{n}: {runs.loc[runs[LABEL] == n, BSSID].nunique()}' for n in names))
rng = np.random.default_rng(0)
res = []
for _ in range(100):
    row = {}
    for n in names:
        g = runs[runs[LABEL] == n]
        aps = g[BSSID].unique()
        pick = rng.choice(aps, min(100, len(aps)), replace=False)
        row[n] = g[g[BSSID].isin(pick)].groupby(BSSID)['filtered_rssi'].mean().mean()
    res.append(row)
res = pd.DataFrame(res)
print('Figure 11 - median of the mean RSSI over 100 repetitions (dBm): ' + ', '.join(f'{n}: {res[n].median():.2f}' for n in names))
plt.figure(figsize=(8, 5))
plt.boxplot([res[n] for n in names]); plt.xticks(range(1, len(names) + 1), [f'Run-{i + 1}' for i in range(len(names))])
plt.xlabel('Run'); plt.ylabel('Mean RSSI (dBm)'); plt.grid(True)
plt.savefig(os.path.join(RESULTS, 'figure11_path_robustness.png'), dpi=200, bbox_inches='tight'); plt.close()

# ---- Figure 12: number of access points per second during the 30-minute city-wide drive (20 February) ----
drive = pd.read_csv(os.path.join(DATA, 'fig12_ap_density/placeA_02-20_city_drive.csv.gz'), low_memory=False)
t = pd.to_datetime(np.floor(timestamps_s(drive['frame.time'])), unit='s')
tod = t - t.dt.normalize()
window = (tod >= pd.Timedelta('18:23:30')) & (tod < pd.Timedelta('18:57:00'))     # the city-wide part of the drive
per_second = drive[window.values].groupby(t[window.values])[BSSID].nunique()
print(f'Figure 12 - drive duration {(per_second.index.max() - per_second.index.min()).total_seconds() / 60:.1f} min, '
      f'median {per_second.median():.0f} APs per second')
plt.figure(figsize=(12, 4))
per_second.plot(marker='o', linestyle='-', markersize=3)
plt.xlabel('Time'); plt.ylabel('Number of Access Points'); plt.grid(True)
plt.savefig(os.path.join(RESULTS, 'figure12_aps_per_second.png'), dpi=200, bbox_inches='tight'); plt.close()
