import pandas as pd
import os
from datetime import datetime

def transform_txt_to_csv(input_path, output_path):
    
    df = pd.read_csv(input_path, delimiter='|')
    
    
    df['join_date'] = pd.to_datetime(df['join_date'])
    df['last_purchase'] = pd.to_datetime(df['last_purchase'])
    df['birth_date'] = pd.to_datetime(df['birth_date'])
    
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    
    df.to_csv(output_path, index=False)
    print(f"File transformed and saved to {output_path}")

if __name__ == "__main__":
    input_file = "data/raw/customers_20230515.txt"
    output_file = "data/processed/customers_20230515.csv"
    transform_txt_to_csv(input_file, output_file)