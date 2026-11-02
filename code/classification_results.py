"""Classification results of the paper: Table 2 (varying leaf density), Table 3 (constant leaf density) and
Table 7 (two selected channels per place).

Usage: python classification_results.py        (run from the code/ folder)
"""
import os
import pandas as pd
from leafsense.classification import classify, dummy_accuracy

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'processed')


def load(path):
    return pd.read_csv(os.path.join(DATA, path), low_memory=False)


def control_oct_oct():
    """Place C, 1 October vs 8 October (two weeks with unchanged foliage), from the weekly 5 GHz data."""
    d = load('placeC_weekly/placeC_weekly_5ghz.csv.gz')
    d = d[d['leaf_status'].isin(['Oct 1st', 'Oct 8th'])].copy()
    d['leaf_status'] = d['leaf_status'].map({'Oct 1st': 'Leaves', 'Oct 8th': 'No Leaves'})   # Week1 / Week2
    return d


TABLE2 = [  # place, band, data
    ('A (May/Feb)', '5 GHz', 'table2/placeA_5ghz_may_feb.csv.gz'),
    ('B (Sep/Feb)', '5 GHz', 'table2/placeB_5ghz_sep_feb.csv.gz'),
    ('C (Oct/Nov)', '5 GHz', 'table2/placeC_5ghz_oct_nov.csv.gz'),
    ('A (May/Feb)', '2.4 GHz', 'table2/placeA_2.4ghz_may_feb.csv.gz'),
    ('B (Sep/Feb)', '2.4 GHz', 'table2/placeB_2.4ghz_sep_feb.csv.gz'),
    ('C (Oct/Nov)', '2.4 GHz', 'table2/placeC_2.4ghz_oct_nov.csv.gz'),
]
TABLE3 = [
    ('B (Feb/Feb)', '5 GHz', 'table3/placeB_5ghz_feb_feb.csv.gz'),
    ('B (Feb/Feb)', '2.4 GHz', 'table3/placeB_2.4ghz_feb_feb.csv.gz'),
    ('C (Oct/Oct)', '5 GHz', control_oct_oct),
]
TABLE7 = [  # place, channels, data
    ('A', [36, 44], 'table2/placeA_5ghz_may_feb.csv.gz'),
    ('B', [44, 48], 'table2/placeB_5ghz_sep_feb.csv.gz'),
    ('C', [36, 149], 'table2/placeC_5ghz_oct_nov.csv.gz'),
]

if __name__ == '__main__':
    for title, rows in (('Table 2 - varying leaf density', TABLE2), ('Table 3 - constant leaf density', TABLE3)):
        print(f'\n{title}\n{"place":13s}{"band":9s}{"RF":>7s}{"DT":>7s}{"DC":>7s}')
        for place, band, src in rows:
            df = src() if callable(src) else load(src)
            rf, dt = classify(df)
            print(f'{place:13s}{band:9s}{rf:6.1f}%{dt:6.1f}%{dummy_accuracy(df):6.1f}%')
    print('\nTable 7 - two selected channels (Random Forest)')
    for place, ch, src in TABLE7:
        rf, _ = classify(load(src), channels=ch)
        print(f'Place {place}  channels {ch[0]} & {ch[1]:<4d} {rf:6.1f}%')
