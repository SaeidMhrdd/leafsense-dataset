"""Apply the filtering pipeline of Section 4.3 to the raw CSV files of one data collection run.

Usage: python process_run.py <raw run folder> <leaf-status label> <output.csv>
Example: python process_run.py ../data/raw/placeB_09-02 Leaves placeB_sep.csv
"""
import glob, os, sys
from leafsense.preprocessing import process_run

if __name__ == '__main__':
    folder, label, out = sys.argv[1], sys.argv[2], sys.argv[3]
    files = sorted(glob.glob(os.path.join(folder, '*.csv.gz')))
    df = process_run(files, label)
    df.to_csv(out, index=False)
    print(f'{len(df)} samples from {df["wlan.bssid"].nunique()} APs written to {out}')
