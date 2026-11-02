# LeafSense: Dataset, Code and Sensing Rig

Data, analysis code and sensing-rig design for

> S. Mehrdad, A. Mohammed and A. Striegel, "LeafSense: Leveraging Wi-Fi Signals for Monitoring Seasonal
> Changes," *Sensors*, 2026.

## Repository structure

| Folder | Content |
|---|---|
| [`data/raw/`](data/raw) | Anonymized records of every data collection run, one file per node (channel) |
| [`data/processed/`](data/processed) | Filtered data sets used for the tables and figures of the paper |
| [`code/`](code) | Filtering pipeline, classification, and the scripts for the tables and figures |
| [`rig/`](rig) | Hardware design and node software of the sensing rig |

The files and columns are described in [`data/README.md`](data/README.md).

## Privacy

* MAC addresses (`wlan.bssid`, `wlan.sa`, `wlan.da`) are replaced by a keyed hash (HMAC-SHA256).
* Only frames transmitted by access points are included. Client device addresses are removed.
* No SSIDs, frame contents or GPS coordinates are included.

## Reproducing the results

Python 3.9, pandas 2.3, NumPy 2.0, scikit-learn 1.6.

```bash
pip install -r code/requirements.txt
cd code
python classification_results.py
python channel_analysis.py
python path_and_density.py
python process_run.py ../data/raw/placeC_11-14 "No Leaves" placeC_nov14.csv
```

Some results in the paper were computed with an earlier version of the window-filtering step and intermediate
files that were not preserved, so values recomputed with the released data and code may differ slightly from those
reported.

## Citation

```bibtex
@article{mehrdad2026leafsense,
  title   = {LeafSense: Leveraging Wi-Fi Signals for Monitoring Seasonal Changes},
  author  = {Mehrdad, Saeid and Mohammed, Alamin and Striegel, Aaron},
  journal = {Sensors},
  year    = {2026}
}

@inproceedings{mehrdad2026leveraging,
  title     = {Leveraging Wi-Fi Signals for Monitoring Seasonal Changes},
  author    = {Mehrdad, Saeid and Mohammed, Alamin and Striegel, Aaron},
  booktitle = {2026 35th International Conference on Computer Communications and Networks (ICCCN)},
  address   = {Honolulu, HI, USA},
  year      = {2026},
  pages     = {1--6},
  doi       = {10.1109/ICCCN69946.2026.11662657}
}
```

## Contact

Saeid Mehrdad, University of Notre Dame — smehrdad@nd.edu
