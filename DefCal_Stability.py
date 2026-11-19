#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Step 1: Import the csv files
file_path_A = r'N:\eProbe_Output\Recipes_Data\X78C\VC\tst-20240516_030711-V325_P180CRU_AD_1DTune_Resort_2p6_D412YBP0_477\ReviewInspection\DeflectionCalibration.log'

#Step 2: Read the csv files into the dataframes and extract the column values
df_A11 = pd.read_csv(file_path_A, delimiter=',', header=2)
median_value = df_A11['Registration_Score'].median()
plus_med = median_value * 1.05
minus_med = median_value * 0.95

#Visualization - Heatmap:
plt.figure(figsize=(10,8))
plt.plot(df_A11['Registration_Score'], marker = 'o', color = 'b')
plt.axhline(y=plus_med, linestyle = '--', color = 'r', label ='Line at 870')
plt.axhline(y=minus_med, linestyle = '--', color = 'g',label ='Line at 920')
plt.title('Defcal stability')
plt.xlabel('Index')
plt.ylabel('DefCal Score')
plt.show()