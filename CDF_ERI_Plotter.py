#!/usr/bin/env python3
import glob
import os.path
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Function to find the file inside the selected folder:
def find_file(root_path, pattern):
    #Find the file based on provided pattern
    for path in glob.glob(os.path.join(root_path, pattern), recursive= True):
        if os.path.isfile(path):
            return os.path.normpath(path)
    return None

#Create a Tkinter root window (hidden):
root = tk.Tk()
root.withdraw()

#Step 1: User input for root path -> Browse:
root_folder = filedialog.askdirectory(title = "Choose the root folder")

#Check if folders are selected:
if root_folder:
    # Choosing the patterned file:
    pattern_1 = os.path.join('fxt*', 'Anl*', 'drilldown', 'CDF','CDF_by_dieIdx.csv')
    #pattern_2 = os.path.join('fxt*', 'Anl*', 'Review*', 'Verified_Review_Plan.csv')
    pattern_2 = os.path.join('fxt*', 'Anl*', 'Rev-*', 'review_plan.csv')
    #pattern_2 = os.path.join('fxt*', 'Anl*', 'Rev-*', 'out*', 'OS_preFilter.csv')

    #Find the files based on pattern:

    CDF_file = find_file(root_folder, pattern_1)
    VRP_file = find_file(root_folder, pattern_2)
    print(CDF_file)
    print(VRP_file)
    #check if files are found and loaded into dataframe:

    if CDF_file:
        df1 = pd.read_csv(CDF_file)
        print("CDF file loaded successfully")
        #print(df1)
    else:
        print("CDF file not found")

    if VRP_file:
        df2 = pd.read_csv(VRP_file, delimiter = ',', header= 16)
        if 'eri_d2d_diff' not in df2.columns:
            df2 = pd.read_csv(VRP_file, delimiter=',', header= 17)
        if 'eri_d2d_diff' not in df2.columns:
            df2 = pd.read_csv(VRP_file, delimiter = ',', header= 0)
        print("VRP file loaded successfully")
    else:
        print("VRP file not found")
else:
    print("No folder selected")
#CDF Plotting:
filtered_data = df1[df1['StddevMultiple'].notna() & (df1['StddevMultiple'] != '') & (df1['parameter'] != 'padMedian')]
plt.figure(figsize=(15,6))
#Visualization - lineplot:
plt.subplot(1,2,1) # 1st row, 2nd column, plot 1
#plt.figure(figsize=(10,8))
plt.xticks(rotation=90)
plt.scatter(filtered_data['bin_def'], filtered_data['StddevMultiple'], s=1, label='CDF')
plt.title('CDF plot')
plt.xlabel('bin_def')
plt.ylabel('StddevMultiple')

#set more points to show on x and y axis:
num_ticks_x = 30
num_ticks_y = 30
#plt.axvline(540, c='r')
#plt.axvline(430, c='g')
plt.xticks(np.linspace(filtered_data['bin_def'].min() - 50, filtered_data['bin_def'].max() + 50, num_ticks_x))
plt.yticks(np.linspace(filtered_data['StddevMultiple'].min() - 1.0, filtered_data['StddevMultiple'].max() + 1.0, num_ticks_y))
plt.grid(True)
plt.legend()

#Visualization - ERI-vs-OS:
plt.subplot(1,2,2) # 1st row, 2nd column, plot 2
#plt.figure(figsize=(10,8))
plt.xticks(rotation=90)
plt.scatter(df2['eri_d2d_diff'], df2['outlierStrength_tail4opens'], s=5, c='r', label='ERI-vs-OS')
#plt.scatter(df2['eri_d2d_diff'], df2['outlierStrength_tail4shorts'], s=20, c='r', label='ERI-vs-OS')
plt.title('ERI-vs-OS plot')
plt.xlabel('Eri D2D')
plt.ylabel('Outlier Strength (Opens)')
#plt.ylabel('Outlier Strength (Shorts)')
plt.xticks(np.linspace(df2['eri_d2d_diff'].min(), df2['eri_d2d_diff'].max(), num_ticks_x))
plt.yticks(np.linspace(df2['outlierStrength_tail4opens'].min(), df2['outlierStrength_tail4opens'].max(), num_ticks_y))
#plt.yticks(np.linspace(df2['outlierStrength_tail4shorts'].min(), df2['outlierStrength_tail4shorts'].max(), num_ticks_y))
plt.grid(True)
plt.legend()

#Show the CDF and ERI-vs-OS plot:
plt.tight_layout() # Adjust spacing between subplots
plt.show()