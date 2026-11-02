"""Classification of the leaf status (Section 5.1 of the paper).

Features per sample: its RSSI, the mean, median, standard deviation, minimum and maximum RSSI of its BSSID,
and the mean RSSI of its channel. The training and test sets are drawn from the samples of each leaf-status
class (80% / 20%). Decision Tree and Random Forest use scikit-learn defaults except for 100 trees in the
Random Forest; the Dummy classifier predicts uniformly at random and serves as the baseline.
"""
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from .preprocessing import RSSI, BSSID, CH, LABEL

FEATURES = ['mean', 'median', 'std', 'min', 'max', RSSI, 'channel_rssi_mean']
TEST_SIZE = 0.2
SEED = 42
N_TREES = 100


def add_features(df, channels=None):
    df = df.copy()
    df[RSSI] = pd.to_numeric(df[RSSI], errors='coerce')
    df = df[df[LABEL].isin(['Leaves', 'No Leaves'])]
    if channels is not None:
        df = df[df[CH].isin(channels)]
    df = df.dropna(subset=[RSSI])
    per_ap = df.groupby(BSSID)[RSSI].agg(['mean', 'median', 'std', 'min', 'max']).reset_index()
    per_ch = df.groupby(CH)[RSSI].mean().rename('channel_rssi_mean').reset_index()
    return df.merge(per_ap, on=BSSID, suffixes=('', '_ap')).merge(per_ch, on=CH)


def classify(df, channels=None, features=None):
    """Returns (Random Forest accuracy, Decision Tree accuracy) in percent."""
    d = add_features(df, channels)
    X = SimpleImputer(strategy='mean').fit_transform(d[features or FEATURES])
    y = d[LABEL]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=TEST_SIZE, stratify=y, random_state=SEED)
    rf = RandomForestClassifier(n_estimators=N_TREES, random_state=SEED).fit(X_tr, y_tr)
    dt = DecisionTreeClassifier(random_state=SEED).fit(X_tr, y_tr)
    return accuracy_score(y_te, rf.predict(X_te)) * 100, accuracy_score(y_te, dt.predict(X_te)) * 100


def dummy_accuracy(df):
    """Baseline: uniform random prediction of the leaf status."""
    d = df[df[LABEL].isin(['Leaves', 'No Leaves'])].copy()
    d[RSSI] = pd.to_numeric(d[RSSI], errors='coerce')
    d = d.dropna(subset=[RSSI])
    y = d[LABEL].map({'Leaves': 1, 'No Leaves': 0})
    X_tr, X_te, y_tr, y_te = train_test_split(d[[RSSI]], y, test_size=0.25, random_state=SEED)
    model = DummyClassifier(strategy='uniform', random_state=SEED).fit(X_tr, y_tr)
    return accuracy_score(y_te, model.predict(X_te)) * 100
