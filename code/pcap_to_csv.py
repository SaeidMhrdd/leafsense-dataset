"""Convert the per-node captures (.pcap) to CSV with tshark (Section 4.2 of the paper).

Usage: python pcap_to_csv.py <folder with .pcap files> <output folder>

The released CSV files were produced with this conversion, then anonymized and restricted to frames transmitted
by access points.
"""
import os, subprocess, sys

FIELDS = ['frame.time', 'wlan.sa', 'wlan.da', 'wlan.bssid', 'wlan_radio.channel', 'radiotap.dbm_antsignal']


def pcap_to_csv(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for name in sorted(os.listdir(input_folder)):
        if not name.endswith('.pcap'):
            continue
        cmd = ['tshark', '-r', os.path.join(input_folder, name), '-T', 'fields']
        for f in FIELDS:
            cmd += ['-e', f]
        cmd += ['-E', 'header=y', '-E', 'separator=,', '-E', 'quote=d', '-E', 'occurrence=f']
        with open(os.path.join(output_folder, name[:-5] + '.csv'), 'w') as out:
            subprocess.run(cmd, stdout=out, check=True)
        print('converted', name)


if __name__ == '__main__':
    pcap_to_csv(sys.argv[1], sys.argv[2])
