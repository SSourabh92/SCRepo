#!/usr/bin/env python3
import glob
import os.path
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.filters.rank import threshold
from sklearn.cluster import DBSCAN
import numpy as np
from scipy.stats import linregress
from tensorflow.python.ops.gen_math_ops import bincount


#Function to find the file inside the selected folder:
def find_file(root_path, pattern):
    #Find the file based on provided pattern
    for path in glob.glob(os.path.join(root_path, pattern), recursive= True):
        if os.path.isfile(path):
            return os.path.normpath(path)
    return None

def read_csv_auto_header(file_path, delimiter=",", headers_to_try=[15,16,17,18]):
    required_cols={"dieIdx", "eri_d2d_diff", "outlierStrength_tail4opens", "outlierStrength_tail4shorts", "padMedian"}
    for header_row in headers_to_try:
        try:
            df = pd.read_csv(file_path, delimiter=delimiter, header=header_row)

            if required_cols.issubset(set(df.columns)):
                print(f"VRP loaded successfully with header = {header_row}")
                return df
        except Exception:
            pass
    print("Coult not read the VRP file with header 15,16,17 or 18")
    return None
def ask_plot_type():
    return messagebox.askyesno("Plot Type", "Plot Opens?\n\nYes = Opens\nNo = Shorts")

def plot_cdf(df1, plot_type):
    # Plot cdf data colored by dieIdx
    filtered_data = df1[df1['StddevMultiple'].notna() & (df1['StddevMultiple'] != '') & (df1['parameter'] != 'padMedian')]
    plt.subplot(1,3,1)
    plt.xticks(rotation=90)

    die_list = sorted(filtered_data["dieIdx"].dropna().unique())
    cmap = plt.colormaps["tab20"]

    for i, die in enumerate(die_list):
        die_data = filtered_data[filtered_data["dieIdx"] == die]
        dist_y= max(die_data["StddevMultiple"])*(die_data["binCount"]/(max(die_data["binCount"])))

        plt.scatter(die_data['bin_def'], die_data['StddevMultiple'], marker=".", s=10, color=cmap(i/max(len(die_list)-1,1)), label=f"Die {die}")

    plt.title("CDF Plot by dieIdx")
    plt.xlabel("bin_def")
    plt.ylabel('StddevMultiple')
    plt.grid(True)
    #AUTO THRESHOLDING:
    #mask = np.isclose(filtered_data["StddevMultiple"], -5.0, rtol=0.01)
    #cluster_array = filtered_data.loc[mask]
    #Nearest neighbour algo:
    #closest_index = np.abs(
    #    cluster_array["bin_def"] - np.median(cluster_array["bin_def"])
    #).argmin()
    #threshold = cluster_array.iloc[closest_index]
# ------------------------------------------------------------------------------------------------
#                       AUTO THRESHOLDING
#------------------------------------------------------------------------------------------------
    # AUTO THRESHOLDING:
    if plot_type:
        sigma = -5
    else:
        sigma = 5

    mask = np.isclose(filtered_data["StddevMultiple"], sigma, rtol=0.01)
    cluster_array = filtered_data.loc[mask]
    # Nearest neighbour algo:
    closest_index = np.abs(
        cluster_array["bin_def"] - np.median(cluster_array["bin_def"])
    ).argmin()
    threshold = cluster_array.iloc[closest_index]
    print(f"Threshold = {threshold[0]}")

#-------------------------------------------------------------------------------------------------
    #Cluster Algo:
    cluster_value = cluster_array.copy()
    eps = cluster_value["bin_def"].diff().abs().median()
    labels = DBSCAN(eps=eps, min_samples=5).fit(cluster_value[["bin_def"]]).labels_ # Try min_sample cluster values between 5 and 20.
    cluster_value["cluster_id"] = labels
    cluster_value = cluster_value[cluster_value["cluster_id"] != -1]
    cluster_summary = (
        cluster_value.groupby(["cluster_id"]).agg(
            count=("bin_def", "count"),
            median_bin=("bin_def", "median")
        )
        .reset_index()
    )
    cluster_summary= (
        cluster_summary.sort_values("count", ascending=False)
        .head(8)
    )
    threshold_new = cluster_summary["median_bin"].quantile(0.97)
    print(cluster_summary)
    print(f"eps = {eps}")
    #print(f"labels = {labels}")
    print(f"Green Threshold = {threshold_new}" )

    plt.scatter(cluster_value["bin_def"], cluster_value["StddevMultiple"], c="red", marker="x", s=10, label="Cluster Value")
    #plt.scatter(cluster_array["bin_def"],cluster_array["StddevMultiple"], c="red", marker=".", s=20, label="Cluster Array" )
    plt.axvline(x=threshold["bin_def"], c="black", linestyle="--", label="Threshold")
    #plt.axvline(x=threshold_new, c="yellow", linestyle="--", label="Threshold")
    u = ["yellow", "magenta", "cyan"]
    for i in range(0,len(cluster_summary["median_bin"])):
        for j in u:
            plt.axvline(x=cluster_summary["median_bin"].iloc[i], c=j, linestyle="-", label="Threshold New")
    #    plt.axvline(x=cluster_summary["median_bin"].iloc[i], c="green", linestyle="-", label="Threshold New")

    plt.subplot(1, 3, 2)
    plt.xticks(rotation=90)
#-----------------------------------------------------------------------------------------------------------------------
#                                               DISTRIBUTION PLOT
#-----------------------------------------------------------------------------------------------------------------------
    for i, die in enumerate(die_list):
        die_data = filtered_data[filtered_data["dieIdx"] == die]
        dist_y = die_data["binCount"]/max(die_data["binCount"])
        plt.plot(die_data["bin_def"], np.log(dist_y), c=cmap(i / max(len(die_list) - 1, 1)), linewidth=2,
                 label="Distribution")
#-----------------------------------------------------------------------------------------------------------------------

    plt.title("Distribution Plot by dieIdx")
    plt.xlabel("bin_def")
    plt.ylabel('binCount')
    plt.grid(True)
    #plt.legend(fontsize=7, bbox_to_anchor=(1.05,1), loc="upper left")


def plot_eri_vs_os(df2, plot_type):
    # Plot erid2d vs OS data colored by dieIdx
    plt.subplot(1, 3, 3)
    plt.xticks(rotation=90)
    die_list = sorted(df2["dieIdx"].dropna().unique())
    cmap = plt.colormaps["tab20"]

    for i, die in enumerate(die_list):
        die_data = df2[df2["dieIdx"] == die]

        if plot_type:
            plt.scatter(die_data['eri_d2d_diff'], die_data['outlierStrength_tail4opens'], s=10, color=cmap(i/max(len(die_list)-1,1)), label=f"die {die}")
        else:
            plt.scatter(die_data['eri_d2d_diff'], die_data['outlierStrength_tail4shorts'], s=10, color=cmap(i/max(len(die_list)-1,1)), label=f"die {die}")
    x= df2['eri_d2d_diff']
    if plot_type:
        y = df2['outlierStrength_tail4opens']
    else:
        y = df2['outlierStrength_tail4shorts']
    slope, intercept, r_value, p_value, std_err = linregress(x,y)
    print(f"Correlation (R) = {r_value:.4f}")
    x_fit = np.linspace(x.min(), x.max(), 100)
    y_fit = slope * x_fit + intercept
    y45 = x_fit
    plt.plot(x_fit,y45)
    plt.plot(x_fit,y_fit,'k--',linewidth=2, label=f'Fit (Corr={r_value:.4f})')
    plt.title("ERI vs OS plot by dieIdx")
    plt.xlabel("erid2d")

    if plot_type:
        plt.ylabel("Outlier Strength Opens")
    else:
        plt.ylabel("Outlier Strength Shorts")

    plt.grid(True)
    #plt.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc="upper left")



def main():
    #Create a Tkinter root window (hidden):
    root = tk.Tk()
    root.withdraw()
    #Step 1: User input for root path -> Browse:
    root_folder = filedialog.askdirectory(title = "Choose the root folder")
    if not root_folder:
        print("No folder selected")
        return
    # Choosing the patterned file:
    pattern_1 = os.path.join('fxt*', 'Anl*', 'drilldown', 'CDF','CDF_by_dieIdx.csv')
    #pattern_2 = os.path.join('fxt*', 'Anl*', 'Review*', 'Verified_Review_Plan.csv')
    pattern_2 = os.path.join('fxt*', 'Anl*', 'Rev-*', 'review_plan.csv')

    #Find the files based on pattern:

    CDF_file = find_file(root_folder, pattern_1)
    VRP_file = find_file(root_folder, pattern_2)
    print("CDF file = ",CDF_file)
    print("Verified Review Plan file = ",VRP_file)

    if not CDF_file:
        print("CDF file not found")
        return
    if not VRP_file:
        print("Verified Review Plan not found")
        return

    df1 = pd.read_csv(CDF_file)
    print("CDF file loaded Successfully")

    df2 = read_csv_auto_header(VRP_file)
    print("Verified Review Plan loaded successfully")

    if df2 is None:
        return
    plot_type = ask_plot_type()
    plt.figure(figsize=(18,6))
    plot_cdf(df1, plot_type)
    plot_eri_vs_os(df2, plot_type)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()