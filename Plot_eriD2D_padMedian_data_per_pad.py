import os.path
import numpy as np
from IPython.core.pylabtools import figsize
from scipy.stats import gaussian_kde
import pandas as pd
import h5py
import matplotlib.pyplot as plt
import gc

from sklearn.utils.extmath import density

toolA_root = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261012_005148-v48_HPRF_Shorts_104D_1Dtune_PBprof\fxt-20261012_005148\Anl-20261012_200026"
toolB_root = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261012_005148-v48_HPRF_Shorts_104D_1Dtune_PBprof\fxt-20261012_005148\Anl-20261012_200026"

dies = ["c010r004"]

##############################
##2X2 plot##
#############################

fig, ax = plt.subplots(1,1, figsize=(8,8))
for die in dies:
    toolA_file = os.path.join(toolA_root, f"{die}.parquet")
    toolB_file = os.path.join(toolB_root, f"{die}.parquet")
    dfA = pd.read_parquet(toolA_file)
    dfB = pd.read_parquet(toolB_file)

    merged = dfA.merge(dfB, on=["DieID", "SwathID", "blockIdx", "localIdx"], suffixes=("_QKT406", "_QKT524"))
    hb = ax.hexbin(merged["erid2d_QKT406"], merged["erid2d_QKT524"], gridsize=200, bins="log", cmap="viridis", mincnt=1)
    # linear fit
    m, b = np.polyfit(merged['erid2d_QKT406'], merged['erid2d_QKT524'], 1)
    gmin = min(merged["erid2d_QKT406"].min(), merged["erid2d_QKT524"].min())
    gmax = max(merged["erid2d_QKT406"].max(), merged["erid2d_QKT524"].max())
    x_fit = np.array([gmin, gmax])
    y_fit = m * x_fit + b
    ax.plot(x_fit, y_fit, color="darkorange", linewidth=2, label="linear fit")
    r = merged["erid2d_QKT406"].corr(merged["erid2d_QKT524"])
    ax.set_title(f"{die}\n" f"r = {r:.5f}\n" f"y = {m:4f}x + {b:.2f}", fontsize=10)
    ##############################################################
    del dfA
    del dfB
    gc.collect()
fig.supxlabel("QKT406 erid2d", fontsize=11)
fig.supylabel("QKT524 erid2d", fontsize=11)
    ###########################################################
    ### HEX PLOT SCRIPT Difference###
    ###########################################################
    # diff = (dfB["GL_median"].astype("int32") - dfA["GL_median"].astype("int32"))
    # hb = ax.hexbin(dfA["GL_median"], diff, gridsize=200, bins="log", cmap="viridis", mincnt=1)
    # # linear fit
    # m, b = np.polyfit(dfA["GL_median"], diff, 1)
    # gmin = min(dfA["GL_median"].min(), dfB["GL_median"].min())
    # xmin = dfA["GL_median"].min()
    # xmax = dfA["GL_median"].max()
    # gmax = max(dfA["GL_median"].max(), dfB["GL_median"].max())
    # x_fit = np.array([xmin, xmax])
    # y_fit = m * x_fit + b
    # ax.plot(x_fit, y_fit, color="darkorange", linewidth=2, label="linear fit")
    # r = dfA["GL_median"].corr(dfB["GL_median"])
    # #ax.set_title(f"{die}\n" f"r = {r:.5f}\n" f"y = {m:4f}x + {b:.2f}", fontsize=10)
    # mean_diff = diff.mean()
    # std_diff = diff.std()
    # print("std_diff = ", std_diff)
    # ax.set_title(f"{die}\n" f"Mean Difference = {mean_diff:4f}\n" f"Difference = {m:.4e}x + {b:.2f}", fontsize=10)
    ##############################################################


    # ###########################################################
    # ### HEX PLOT SCRIPT ###
    # ###########################################################

    # hb = ax.hexbin(dfA["GL_median"], dfB["GL_median"], gridsize=200, bins="log", cmap="viridis", mincnt=1)
    #
    # # linear fit
    # m, b = np.polyfit(dfA["GL_median"], dfB["GL_median"], 1)
    # gmin = min(dfA["GL_median"].min(), dfB["GL_median"].min())
    # xmin = dfA["GL_median"].min()
    # xmax = dfA["GL_median"].max()
    # gmax = max(dfA["GL_median"].max(), dfB["GL_median"].max())
    # x_fit = np.array([gmin, gmax])
    # y_fit = m * x_fit + b
    # ax.plot(x_fit, y_fit, color="darkorange", linewidth=2, label="linear fit")
    # r = dfA["GL_median"].corr(dfB["GL_median"])
    # ax.set_title(f"{die}\n" f"r = {r:.5f}\n" f"y = {m:4f}x + {b:.2f}", fontsize=10)

#     ##############################################################
#     del dfA
#     del dfB
#     gc.collect()
# fig.supxlabel("QKT406 pad Median GL", fontsize=11)
# fig.supylabel("QKT524 GL padMedian", fontsize=11)

plt.tight_layout()
plt.savefig(r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261012_005148-v48_HPRF_Shorts_104D_1Dtune_PBprof\fxt-20261012_005148\Anl-20261012_200026\QKT406_QKT524_erid2d_c010r004.png", dpi=300, bbox_inches="tight")
plt.show()