# LeafSense Dataset and Sensing Rig

Data and hardware design from **LeafSense** (Saeid Mehrdad, Alamin Mohammed, Aaron Striegel —
University of Notre Dame).

LeafSense infers the presence or absence of leaves on street trees from variations in the
received signal strength (RSSI) of beacon frames broadcast by existing residential Wi-Fi
access points, captured from a moving vehicle. No new transmitters and no cooperation from
the access points are required.

## Contents

| Path | What it holds |
|---|---|
| `data/` | Anonymized per-run CSV captures (see schema below) — *pending upload* |
| `rig/` | Sensing-rig design: bill of materials, wiring/component diagram, node roles |
| `scripts/` | Capture and preprocessing scripts (pcap → CSV, filtering pipeline) — *pending upload* |

## Dataset summary

Collected across three residential areas of a mid-sized Midwestern US city, from a vehicle
driven at a steady 20–30 mph, on 11 Wi-Fi channels (2.4 GHz: 1, 6, 11; 5 GHz: 36, 40, 44,
48, 149, 153, 157, 161).

| Place | Months | Band | BSSIDs (raw / filtered) | Samples (raw / filtered) |
|---|---|---|---|---|
| A | May, Feb | 5 GHz | 949 / 527 · 1072 / 543 | 74,185 / 30,818 · 86,381 / 33,793 |
| A | May, Feb | 2.4 GHz | 247 / 50 · 100 / 33 | 6,527 / 2,161 · 2,644 / 879 |
| B | Sep, Feb | 5 GHz | 201 / 129 · 358 / 160 | 18,346 / 9,733 · 25,861 / 10,005 |
| B | Sep, Feb | 2.4 GHz | 48 / 12 · 124 / 19 | 981 / 389 · 2,292 / 613 |
| C | Oct, Nov (weekly) | 5 GHz | 210 / 158 · 331 / 252 | 39,421 / 13,396 · 70,426 / 25,019 |
| C | Oct, Nov (weekly) | 2.4 GHz | 69 / 24 · 131 / 65 | 4,032 / 785 · 8,514 / 2,442 |

Totals: **339,610** RSSI samples from **3,840** unique access points before filtering;
**130,033** samples from **1,972** access points after the filtering pipeline described in the paper.

## Data schema

Each run is a CSV converted from the original pcap capture. Columns:

| Column | Meaning |
|---|---|
| `frame.time` | Capture timestamp |
| `wlan.sa` | Source (transmitter) address — **hashed** |
| `wlan.da` | Destination address (always `ff:ff:ff:ff:ff:ff` for beacons) |
| `wlan.bssid` | BSSID — **hashed** |
| `radiotap.dbm_antsignal` | RSSI in dBm, as reported by the radiotap header (spurious values retained; see paper) |
| `channel` | Wi-Fi channel the capturing node was tuned to |
| `lat`, `lon` | GPS position — **transformed** (see Anonymization) |

Only beacon frames were captured. No data frames were recorded at any point.

## Anonymization

- **BSSID and source MAC** are replaced by a keyed hash. The mapping is not released.
- **SSID** is not included.
- **Location** is passed through a privacy-preserving transformation that preserves relative
  geometry within a run but does not recover absolute street addresses.
- **No data frames** were captured or retained; only management (beacon) frames.

## Sensing rig

Thirteen Raspberry Pi 4 nodes on an Ethernet switch: 11 capture nodes, one per channel, each
with a USB Wi-Fi adapter in monitor mode and an external antenna; one node with a
BerryGPS-IMU v3 for GPS; one head node acting as MQTT broker for time synchronization and
data aggregation. The paper also describes a minimal two-channel variant on a single Pi.
Design files are in `rig/`.

## Citation

Journal version (under review):

```bibtex
@article{mehrdad2026leafsense,
  title   = {LeafSense: Leveraging Wi-Fi Signals for Monitoring Seasonal Changes},
  author  = {Mehrdad, Saeid and Mohammed, Alamin and Striegel, Aaron},
  journal = {},
  year    = {},
  volume  = {},
  pages   = {},
  doi     = {}
}
```

Conference version:

```bibtex
@inproceedings{mehrdad2026leveraging,
  title     = {Leveraging Wi-Fi Signals for Monitoring Seasonal Changes},
  author    = {Mehrdad, Saeid and Mohammed, Alamin and Striegel, Aaron},
  booktitle = {2026 35th International Conference on Computer Communications and Networks (ICCCN)},
  year      = {2026}
}
```

## Contact

Saeid Mehrdad — smehrdad@nd.edu
