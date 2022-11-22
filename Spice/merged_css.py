import os
import pandas as pd

merged_df = pd.DataFrame()

for file in os.listdir(os.getcwd()):
    if file.endswith('.csv'):
        merged_df = pd.concat([pd.read_csv(file)])

merged_df.to_csv('merged csv.csv', index=False)

