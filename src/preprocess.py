import pandas as pd
def preprocess(df): 
    
#    Preprocess the input DataFrame by performing the following steps:
 #   1. Standrdize column names 
 df.columns = df.columns.str.lower().str.strip()

 #Conver dates

 for col in df.columns:
    if 'date' in col:
        df[col] = pd.to_datetime(df[col], errors='coerce')      

    # fill missing numeric values

    numeric_cols = df.select_dtypes(include=['number']).columns

    df[numeric_cols]= df[numeric_cols].fillna(0)     


    # Fill missing categorical values
    object_cols = df.select_dtypes(include=object).columns
    df[object_cols] = df[object_cols].fillna('Unknown')

    return df

    