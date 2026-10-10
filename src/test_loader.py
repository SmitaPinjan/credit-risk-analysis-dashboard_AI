from loader import load_csv

df = load_csv("loan_portfolio.csv")
print(df.head())
print(df.shape)

