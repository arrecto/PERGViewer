'''import os
import pandas as pd

folder_path = "C:/Users/Allen Ivan/Downloads/Thesis_opthal/thesis-database/a-comprehensive-dataset-of-pattern-electroretinograms-for-ocular-electrophysiology-research-the-perg-ioba-dataset-1.0.0/csv"
def get_csv_files_in_folder(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    return csv_files

csv_files = get_csv_files_in_folder(folder_path)

csv_col = []
for i in csv_files:
    df = pd.read_csv(i)
    csv_col.append(len(df.columns)//3)
print(max(csv_col))

print(pd.Series(csv_col).value_counts())'''
import numpy as np
c = [4,23,54,7,9,7,0,0,2]
c = np.array(c)
max = max(c)
min=min(c)
a = 2*(c-0.5*(max+min))/(0.5*(max-min))
b =((c-min)/(max-min))*(2-(-2))+(-2)
print(a)
print(b)