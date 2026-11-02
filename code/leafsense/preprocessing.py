"""Data preparation and filtering (Section 4 of the paper).

Pipeline for one data collection run:
    prepare()        -> drop incomplete rows, drop the broadcast BSSID, keep frames whose source address equals the BSSID
    select_aps()     -> keep APs with at least 30 samples, then DBSCAN on the capture time to separate repeated
                        passes and keep, for each AP, the pass closest to the AP
    window_filter()  -> 1 dB/s filter on one-second mean RSSI that removes samples recorded while the vehicle
                        was stationary
"""
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

RSSI, BSSID, CH, LABEL = 'radiotap.dbm_antsignal', 'wlan.bssid', 'wlan_radio.channel', 'leaf_status'
BROADCAST = 'ff:ff:ff:ff:ff:ff'

MIN_SAMPLES_PER_AP = 30     # Section 4.3.1
DBSCAN_EPS_S = 10           # Section 4.3.2: capture time in seconds, eps = 10 s
DBSCAN_MIN_SAMPLES = 50     #                min_samples = 50
TOP_FRACTION = 0.10         # cluster whose top 10% RSSI values have the highest mean is retained
WINDOW_S = 1                # one-second windows
WINDOW_DB = 1.0             # change of at least 1 dB between consecutive windows


def timestamps_s(frame_time):
    """Seconds from the 'frame.time' strings ('Mon DD HH:MM:SS.fffffffff'; the year is not included)."""
    t = pd.to_datetime('2000 ' + frame_time.astype(str), format='%Y %b %d %H:%M:%S.%f', errors='coerce')
    return t.astype('int64') / 1e9


def prepare(df):
    """Section 4.2: data cleansing."""
    df = df.copy()
    df[RSSI] = pd.to_numeric(df[RSSI], errors='coerce')
    df = df.dropna(subset=['frame.time', 'wlan.sa', BSSID, RSSI])
    df = df[df[BSSID] != BROADCAST]
    df = df[df['wlan.sa'] == df[BSSID]]
    return df.reset_index(drop=True)


def select_aps(df):
    """Sections 4.3.1-4.3.2: AP selection and DBSCAN filtering of repeated passes."""
    df = df.groupby(BSSID).filter(lambda x: len(x) >= MIN_SAMPLES_PER_AP).copy()
    df['_t'] = timestamps_s(df['frame.time'])
    kept = []
    for _, g in df.groupby(BSSID):
        labels = DBSCAN(eps=DBSCAN_EPS_S, min_samples=DBSCAN_MIN_SAMPLES).fit(g[['_t']].values).labels_
        g = g.assign(cluster=labels)
        if g['cluster'].nunique() == 1:                 # a single pass: all samples are kept
            kept.append(g)
            continue
        best, best_value = None, -np.inf                 # several passes: keep the one closest to the AP
        for c in g['cluster'].unique():
            if c == -1:                                  # DBSCAN noise
                continue
            r = g.loc[g['cluster'] == c, RSSI]
            value = r.nlargest(max(1, int(TOP_FRACTION * len(r)))).mean()
            if value > best_value:
                best, best_value = c, value
        if best is not None:
            kept.append(g[g['cluster'] == best])
    return pd.concat(kept, ignore_index=True).drop(columns='_t')


def window_filter(df, by=(LABEL, BSSID)):
    """Section 4.3.2: keep the one-second windows in which the mean RSSI rises by at least 1 dB while the
    vehicle approaches the AP and falls by at least 1 dB after the peak; windows with a smaller change
    (stationary vehicle) are discarded."""
    out = []
    for _, g in df.groupby(list(by)):
        g = g.copy()
        t = timestamps_s(g['frame.time'])
        g['time_bin'] = ((t - t.min()) // WINDOW_S).astype(int)
        means = g.groupby('time_bin')[RSSI].mean().dropna()
        bins, vals = means.index.values, means.values
        if len(vals) == 0:
            continue
        peak = int(np.argmax(vals))
        ref, keep = vals[0], [bins[0]]
        for i in range(1, peak):
            if vals[i] >= ref + WINDOW_DB:
                keep.append(bins[i]); ref = vals[i]
        keep.append(bins[peak]); ref = vals[peak]
        for i in range(peak + 1, len(vals)):
            if vals[i] <= ref - WINDOW_DB:
                keep.append(bins[i]); ref = vals[i]
        out.append(g[g['time_bin'].isin(keep)])
    return pd.concat(out, ignore_index=True)


def process_run(raw_files, label):
    """Full pipeline for one run: list of per-Pi CSV files -> filtered samples with a leaf-status label."""
    df = pd.concat([pd.read_csv(f, low_memory=False) for f in raw_files], ignore_index=True)
    df = select_aps(prepare(df))
    df[LABEL] = label
    return window_filter(df)
