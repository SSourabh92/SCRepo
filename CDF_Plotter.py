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
file_path = filedialog.askopenfilename(title = "Choose the CDF file", filetypes = [("CSV files", "*.csv")])

#Step 2: Read the csv files into the dataframes and extract the column values
df_data = pd.read_csv(file_path, delimiter=',', header=0)
filtered_data = df_data[df_data['StddevMultiple'].notna() & (df_data['StddevMultiple'] != '') & (df_data['parameter'] != 'padMedian')]

#Visualization - lineplot:
plt.figure(figsize=(10,8))
plt.xticks(rotation=90)
plt.scatter(filtered_data['bin_def'], filtered_data['StddevMultiple'], s=3, c= 'blue', label = 'CDF')
plt.title('CDF plot')
plt.xlabel('bin_def')
plt.ylabel('StddevMultiple')

#set more points to show on x and y axis:
num_ticks_x = 20
num_ticks_y = 20
plt.xticks(np.linspace(filtered_data['bin_def'].min() - 50, filtered_data['bin_def'].max() + 50, num_ticks_x))
plt.yticks(np.linspace(filtered_data['StddevMultiple'].min() - 1.0, filtered_data['StddevMultiple'].max() + 1.0, num_ticks_y))
plt.grid(True)
plt.legend()
#Show the CDF plot:
plt.show()