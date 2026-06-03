import pandas as pd
import sys

try:
    df = pd.read_excel(r'..\backend\data\Catálogo Sepomex.xlsx', skiprows=2, nrows=5)
    print(df.columns.tolist())
    print(df.head())
except Exception as e:
    print(f"Error: {e}")
