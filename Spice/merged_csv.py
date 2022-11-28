import os
import pandas as pd
import time

master_df = pd.DataFrame()

for file in os.listdir(os.getcwd()):
    if file.endswith('.csv'):
        master_df = master_df.append(pd.read_csv(file))
        print(file)

master_df.to_csv('merged_csv.csv', index=False)
