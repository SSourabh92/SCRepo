import h5py
import argparse
from pathlib import  Path
import pandas as pd
import tkinter as tk
from tkinter import filedialog

#Create a hidden root window
root = tk.Tk()
root.withdraw()

#Open file dialog to select the Attribute CSV file

#file_path = filedialog.askopenfilename(title= "Select the h5 file", initialdir= "N:\eProbe_Setup\Recipe-Repo\Measurment\InspectionTest", filetypes=[("h5 Files", "*.h5")])
file_path = r'N:\eProbe_Setup\Recipe-Repo\Measurment\InspectionTest\X802B\V1\Tuning\v21_88D_1Dtune_resort.h5'
def print_h5_keys(h5_path: Path):
    with h5py.File(h5_path,'r') as store:
        keys = store.keys()
        data = store["Swaths"]
        if not keys:
            print("[H5] No keys found.")
        else:
            print("[H5] Keys found:")
            for k in keys:
                print(" ", k)
            print(data)
    return

def print_swaths(h5_path):
    with h5py.File(h5_path,'r') as store:
        if "Tables" not in store:
            print("[H5] 'Swaths group not found")
        else:
            swaths_group = store["Tables"]
            for name in swaths_group.keys():
                print(" -", name)
    return

print(print_h5_keys(file_path))
print(print_swaths(file_path))