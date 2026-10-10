import pandas as pd
import os

DATA_DIR = "data"

def load_csv(filename):
    """
    Generic loader for any CSV file in the data folder.
    Example: load_csv("loan_portfolio.csv")
    """
    path = os.path.join(DATA_DIR, filename)
    return pd.read_csv(path)



