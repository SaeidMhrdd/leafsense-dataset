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

| Folder | Place | Date | Role in the paper | Channels |
|---|---|---|---|---|
| `placeA_05-15` | A | 15 May | "Leaves" | 1, 6, 11, 36, 40, 44, 48, 153, 157 |
| `placeA_02-20` | A | 20 Feb | "No Leaves"; also the city-wide drive of Figure 12 | all 11 |
| `placeB_09-02` | B | 2 Sep | "Leaves" (two passes) | all 11 |
| `placeB_02-01` | B | 1 Feb | "No Leaves"; week 1 of the constant-leaf control | all 11 |
| `placeB_02-03` | B | 3 Feb | week 2 of the constant-leaf control | all 11 |
| `placeC_10-01` | C | 1 Oct | "Leaves"; week 1 of the constant-leaf control | all 11 |
| `placeC_10-08` | C | 8 Oct | week 2 of the constant-leaf control | all except 149 |
| `placeC_10-22` | C | 22 Oct | weekly run | all except 149 |
| `placeC_10-30` | C | 30 Oct | weekly run | all 11 |
| `placeC_11-08` | C | 8 Nov | weekly run | all 11 |
| `placeC_11-14` | C | 14 Nov | "No Leaves" | all 11 |
| `placeC_04-04` | C | 4 Apr | five runs for the path-robustness analysis (Figure 11) | 11, 36, 40, 44, 48, 153, 157, 161 |

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
