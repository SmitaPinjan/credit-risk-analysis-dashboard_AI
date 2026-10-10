# from loader import load_csv
# from preprocess import preprocess
# from risk_engine import risk_signals

# df = load_csv("loan_portfolio.csv")
# df = preprocess(df)
# signals = risk_signals(df)

# print(signals)

import sys
sys.path.append("src")

from loader import load_csv
from preprocess import preprocess
from risk_engine import risk_signals
import pandas as pd

df = pd.read_csv("data/loan_portfolio.csv", engine="python", on_bad_lines="skip")

print(risk_signals(df))



