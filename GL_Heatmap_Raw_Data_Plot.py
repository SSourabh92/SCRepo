import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt

# Loading the pad list in the sequence used by FPGA:
with h5py.File(r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20260613_093447-V17_56D_35S_Tuned\V17_56D_35S_Tuned.h5") as f:
    #read the swath dataset table
    swath_table = f['Swaths/X78D-H20009#0'][:]
    block_indices = swath_table['blockIdx']
    local_indices = swath_table['localIdx']
    pad_raster_indices = swath_table['padRasterIdx']

# Importing and reading the binary file using numpy:
# Median file: 1 per table row
median_bin = np.fromfile(r"N:\eProbe_Output\Recipeas_Data\X78D\VC\tst-20260613_093447-V17_56D_35S_Tuned\fxt-20260613_093447\c005r006\X78D-H20009#0\median.bin", dtype=np.uint16)
# Raw file: 80 per table row
raw_greyLevel = np.fromfile(r"M:\eProbe_Output\Recipes_Data\X78D\VC\tst-20260613_093447-V17_56D_35S_Tuned\c005r006\X78D-H20009#0.sth2", dtype=np.uint16)
raw_matrix = raw_greyLevel.reshape((len(median_bin), 80))
#Converting to Pandas
#df_median_bin = pd.DataFrame(median_bin, columns=["GL_MedianSignalPerPad"]) # 1 x no. of pads
#df_raw_greyLevel = pd.DataFrame(raw_greyLevel, columns=["Raw_GL_SignalPerPixel"]) #80 x no. of pads so basically 1 point per pixel as per raster
#df["Moving_Average"] = df["GL_median(tiles)"].rolling(5000).mean()
print("raw matrix shape = ", raw_matrix.shape)

# Analysis of Raw Data:
# target_localIdx = [410, 411]
target_localIdx = [410, 411]
target_blockIdx = 1009002
# Find all matching row indices in the table where this localIdx appears
matching_rows = np.where(np.isin(local_indices,target_localIdx) & (block_indices == target_blockIdx))[0]
#matching_rows = np.where(block_indices == target_blockIdx)[0]
print(f"Found {len(matching_rows)} occurrences for localIdx {target_localIdx} at row indices: {matching_rows}:")

#Analysing the pad level grey level for a specific pad. Get all 80 points for this specific pad instance:
for row_idx in matching_rows:
    print(f"\t Analysing the table row {row_idx}:")
    raw_points = raw_matrix[row_idx, :]
    #raw_points_1 = raw_matrix[row_idx, 10:70 ]
    print(f"\t Median padGL =  {np.median(raw_points)}")
    print(f"\t Median padGL =  {np.median(raw_points_1)}")
    #plt.plot(raw_points_1, label=f'{row_idx} ({target_blockIdx})')
    plt.plot(raw_points, label=f'{row_idx} ({target_blockIdx})')

# print(f"\t Median padGL =  {np.median(raw_points)}")
# print(f"\t Median padGL from median.bin file =  {median_bin[0]}")

#raw_points = pd.DataFrame(raw_matrix[matching_rows,:], columns=["GLSignal"])
#plt.plot(raw_points)
plt.show()

#Analysis for a tile:
# tile_raw_data = raw_matrix[matching_rows, 10:70]
# plt.figure(figsize=[8,8])
# plt.imshow(tile_raw_data, aspect='auto', cmap='viridis', interpolation='nearest')
# plt.colorbar(label='raw GL Value')
# plt.title(f'Raw Data Heatmap for Tile: {target_blockIdx} (Pads vs 80 Scan points)')
# plt.xlabel('Raw Scan points (0 to 79)')
# plt.ylabel('Pad Index within Tile')
# plt.show()


