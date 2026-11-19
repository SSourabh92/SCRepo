import os.path
import numpy as np
from scipy.stats import gaussian_kde
import pandas as pd
import h5py
import matplotlib.pyplot as plt
import gc

from sklearn.utils.extmath import density

toolA_root = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261012_005148-v48_HPRF_Shorts_104D_1Dtune_PBprof\fxt-20261012_005148"
toolB_root = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261015_195701-v49_HPRF_Shorts_24D_1Dtune_CDF_check_Arizona\fxt-20261015_195701"

dies = ["c012r004"]
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
#dies = ["c010r004", "c011r005", "c012r004", "c013r005"]
merge_cols = ['blockIdx', 'localIdx', 'Swath']
##############################
##2X2 plot##
#############################

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=[12,10], sharex=True, sharey=True)
for die, ax in zip(dies, axes.flatten()):
    print(f"pProcessing {die}")
    toolA_file = os.path.join(toolA_root, die, f"{die}.parquet")
    toolB_file = os.path.join(toolB_root, die, f"{die}.parquet")
    dfA = pd.read_parquet(toolA_file)
    dfB = pd.read_parquet(toolB_file)
    df_merged = dfA.merge(dfB, on=merge_cols, suffixes=("_QKT406", "_QKT524"))
    df_merged['ratio'] = df_merged['GL_median_QKT524'] / df_merged['GL_median_QKT406']
    #df_merged_filtered = df_merged[(df_merged["ratio"] >= 1.159) & (df_merged["ratio"] <= 1.161 ) & (df_merged["GL_median_QKT406"] >= 5800) & (df_merged["GL_median_QKT406"] <= 5850)]
    df_merged_filtered = df_merged[(df_merged["ratio"].between(1.2099,1.2199, inclusive="neither")) & (df_merged["GL_median_QKT406"].between(5248,5251, inclusive="neither")) ]
    #print(df_merged_filtered.columns)
    print(df_merged_filtered)