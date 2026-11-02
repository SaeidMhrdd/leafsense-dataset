# Data

All files are gzip-compressed CSV (`.csv.gz`). MAC addresses are anonymized as described in the main
[README](../README.md#privacy).

## Columns

| Column | Description |
|---|---|
| `frame.time` | Capture time, as written by tshark (rig clock) |
| `wlan.sa` | Source address (anonymized) |
| `wlan.da` | Destination address: `ff:ff:ff:ff:ff:ff` for broadcast frames, empty otherwise |
| `wlan.bssid` | BSSID of the access point (anonymized) |
| `wlan_radio.channel` | Wi-Fi channel of the node that captured the frame |
| `radiotap.dbm_antsignal` | RSSI (dBm) |

Processed files contain, in addition:

| Column | Description |
|---|---|
| `leaf_status` | Label: `Leaves` / `No Leaves` for the seasonal comparisons; the date of the run (e.g. `Oct 1st`) for the weekly data of Place C; the run (`split-1` … `split-5`) for Figure 11 |
| `cluster` | DBSCAN cluster of the sample (Section 4.3.2) |
| `time_bin` | Index of the one-second window used by the 1 dB/s filter |
| `filtered_rssi` | RSSI retained by the 1 dB/s filter |

## `raw/`

One folder per run and one file per node, named `ch<channel>_<date>_<start time>.csv.gz`.

## `processed/`

| File | Used for |
|---|---|
| `table2/placeA_5ghz_may_feb.csv.gz` | Table 2, Place A, 5 GHz; Table 7, Place A |
| `table2/placeA_2.4ghz_may_feb.csv.gz` | Table 2, Place A, 2.4 GHz |
| `table2/placeB_5ghz_sep_feb.csv.gz` | Table 2, Place B, 5 GHz; Table 7, Place B; Figures 6 and 7 |
| `table2/placeB_2.4ghz_sep_feb.csv.gz` | Table 2, Place B, 2.4 GHz |
| `table2/placeC_5ghz_oct_nov.csv.gz` | Table 2, Place C, 5 GHz; Table 7, Place C |
| `table2/placeC_2.4ghz_oct_nov.csv.gz` | Table 2, Place C, 2.4 GHz; Table 6 (1 October, 2.4 GHz) |
| `table3/placeB_5ghz_feb_feb.csv.gz` | Table 3, Place B, 5 GHz |
| `table3/placeB_2.4ghz_feb_feb.csv.gz` | Table 3, Place B, 2.4 GHz |
| `placeC_weekly/placeC_weekly_5ghz.csv.gz` | Table 3, Place C; Table 6; Figures 9 and 10 |
| `placeC_weekly/placeC_weekly_2.4ghz.csv.gz` | Table 6 |
| `fig11_path_robustness/placeC_04-04_five_runs.csv.gz` | Figure 11 |
| `fig12_ap_density/placeA_02-20_city_drive.csv.gz` | Figure 12 |

Tables 4 and 5 are computed from `raw/placeC_*`.
