import pandas as pd
import tkinter as tk
from tkinter import filedialog

#Create a hidden root window
root = tk.Tk()
root.withdraw()

#Open file dialog to select the Attribute CSV file

file_path = filedialog.askopenfilename(title= "Select the CSV file", filetypes=[("CSV Files", "*.csv")])
#Read the file as a dataframe
df = pd.read_csv(file_path, low_memory=False)
#print(df.head())

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#THIS IS THE MAIN FILTER THAT DECIDES HOW THE failModeId NEEDS TO BE CREATED#

df['failModeID'] = 'VTALL' + df['VT_allCount'].fillna(0).astype(float).astype(int).astype(str) + '_' + 'VGALL' + df['VG_allCount'].astype(str)

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

#Save to new file
save_path = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV Files", "*.csv")],title="Save the new prior file as")
df.to_csv(save_path, index=False)
uniqueFMIDsavepath = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV Files", "*.csv")],title="Save the unique FMID file as")
pd.DataFrame(df['failModeID'].dropna().unique(),columns=['uniqueFMID']).to_csv(uniqueFMIDsavepath, index=False)
print(df['failModeID'].unique())