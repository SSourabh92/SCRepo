#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Create a Tkinter root window
root = tk.Tk()
root.withdraw()

#Step 1: User input for file path->Browse:
#file_path = filedialog.askopenfilename(title = "Choose the CDF file", filetypes = [("CSV files", "*.csv")])

#Dataset 1

file_path = r"N:\eProbe_Output\Recipes_Data\X78Er\VC\tst-20260512_184304-v3_56D_1DTune\fxt-20260512_184304\Anl-20260512_211547\Rev-20260512_220923\outliers_dir\stg2_OutlierCnt_after_die_exclusion.csv"
#Step 2: Read the csv files into the dataframes and extract the column values
df_data = pd.read_csv(file_path, delimiter=',', header=0)
print(df_data.head())
GLMedian = df_data["padMedian"].median()
heatmap_data = df_data.pivot_table(index = "padCentX", columns = "padCentY", values = "padMedian", aggfunc = "median")
BinSize = 3 # we can try different size like 2, 3, 4, 5, etc.
df_data["x_bin"] = (df_data["padCentX"] // BinSize).astype(int)
df_data["y_bin"] = (df_data["padCentY"] // BinSize).astype(int)
binned_heatmap = df_data.pivot_table(index = "x_bin", columns = "y_bin", values = "padMedian", aggfunc = "median")
percentage_deviation = 100 * (GLMedian - binned_heatmap)/GLMedian

#Dataset 2

file_path2 = r"N:\eProbe_Output\Recipes_Data\X78Er\VC\tst-20260512_184304-v3_56D_1DTune\fxt-20260512_184304\Anl-20260512_211547\Rev-20260512_220923\outliers_dir\stg2_OutlierCnt_after_die_exclusion.csv"
#Step 2: Read the csv files into the dataframes and extract the column values
df_data2 = pd.read_csv(file_path2, delimiter=',', header=0)
print(df_data2.head())
GLMedian2 = df_data2["padMedian"].median()
heatmap_data2 = df_data2.pivot_table(index = "padCentX", columns = "padCentY", values = "padMedian", aggfunc = "median")
BinSize2 = 3 # we can try different size like 2, 3, 4, 5, etc.
df_data2["x_bin"] = (df_data2["padCentX"] // BinSize2).astype(int)
df_data2["y_bin"] = (df_data2["padCentY"] // BinSize2).astype(int)
binned_heatmap2 = df_data2.pivot_table(index = "x_bin", columns = "y_bin", values = "padMedian", aggfunc = "median")
percentage_deviation2 = 100 * (GLMedian2 - binned_heatmap2)/GLMedian2

all_val = np.concatenate([percentage_deviation.values.flatten(), percentage_deviation2.values.flatten()])
all_val = all_val[~np.isnan(all_val)]
vmax = np.max(np.abs(all_val))
vmax = min(vmax, 25)
fig, axes = plt.subplots(1,2, figsize = (14,6), sharex=True, sharey=True)
sns.heatmap(percentage_deviation, cmap="RdBu_r", center = 0, vmin= -vmax, vmax=vmax, cbar_kws={"label": "GL % deviation"}, ax=axes[0])
axes[0].set_title("X78E M2 Old")
sns.heatmap(percentage_deviation2, cmap="RdBu_r", center = 0, vmin= -vmax, vmax=vmax, cbar_kws={"label": "GL % deviation"}, ax=axes[1])
axes[1].set_title("X78E M2 New")
plt.show()