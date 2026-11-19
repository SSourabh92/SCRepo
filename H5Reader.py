import h5py
import pandas as pd
import tkinter as tk
from tkinter import filedialog

#Create a hidden root window
root = tk.Tk()
root.withdraw()

#Open file dialog to select the Attribute CSV file

file_path = filedialog.askopenfilename(title= "Select the h5 file", initialdir= "N:\eProbe_Setup\Collateral", filetypes=[("h5 Files", "*.h5")])
#file_path = r'N:\eProbe_Setup\Collateral\GNRB\M5\Rcp_collat_20250811_173627\eProbe250-RcpCol-v2.2_rid-UTC-20250812-004827_GNRB-M5_WS-20250731_R1.h5'
with h5py.File(file_path,'r') as file:
    data = file['DFI_Pad_Care/WS/LUT/failModeID'][:]
    print("failModeID: ", data)