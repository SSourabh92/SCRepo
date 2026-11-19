import h5py
import pandas as pd
import tkinter as tk
from tkinter import filedialog

#Create a hidden root window
root = tk.Tk()
root.withdraw()

#Open file dialog to select the Attribute CSV file

file_path = filedialog.askopenfilename(title= "Select the h5 file", initialdir= "N:\eProbe_Output\Recipes_Data", filetypes=[("h5 Files", "*.h5")])
#file_path = r'N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20250402_001737-v12_X78D_VC_P180_HVT_RVT_112D_1Dtune\v12_X78D_VC_P180_HVT_RVT_112D_1Dtune.h5'

with h5py.File(file_path,'r') as file:
    data = file['Tables/Swath_Plan'][:]
    dut_data= file['Tables/RasterStatistics'][:]
    column_names = list(file['Tables/Swath_Plan'].attrs['columns']) if 'columns' in file['Tables/Swath_Plan'].attrs else None
    dut_column_names = list(file['Tables/RasterStatistics'].attrs['columns']) if 'columns' in file['Tables/RasterStatistics'].attrs else None

df = pd.DataFrame(data, columns=column_names)
df_dut = pd.DataFrame(dut_data, columns=dut_column_names)
#print("column names: ", df.columns.tolist())
#print(df)

# calculate the new columns to create coordinates for Lower (X,Y) and Upper (X,Y) of the diagonal of rectangle, irrespective of swath orientation

df['LL_X'] = df[['Start X', 'End X']].min(axis=1) - 20
df['LL_Y'] = df[['Start Y', 'End Y']].min(axis=1) - 20
df['UR_X'] = df[['Start X', 'End X']].max(axis=1) + 20
df['UR_Y'] = df[['Start Y', 'End Y']].max(axis=1) + 20

#Bounding box csv file:
df['swathId'] = df['swathId'].str.decode('utf-8')
bounding_box_df = df[['swathId','LL_X', 'LL_Y', 'UR_X', 'UR_Y']]
#bounding_box_df.to_csv('BBcoordinates.csv', index=False)
df['Swath_Area'] = (df['UR_X']-df['LL_X']) * (df['UR_Y']-df['LL_Y'])/(100000000)
print(df)
NumberofDies = 128
Total_swath_Area = sum(df['Swath_Area'])
print("Total Number of Dies per Wafer =", NumberofDies)
print("Total DUT count per Die (M) =", df_dut['padCount'][0]/1000000)
print("Total DUT count per Wafer (B) =", df_dut['padCount'][0]*NumberofDies/1000000000)
print("Total Swath Area (cm^2) per Die =", Total_swath_Area)
print("Total Swath Area (cm^2) per Wafer =", Total_swath_Area * NumberofDies)
print("B-DUTs per unit Area (cm^2)=", ((df_dut['padCount'][0]) / (1000000000))/(Total_swath_Area))
#print(bounding_box_df)