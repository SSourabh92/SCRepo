import os.path
import numpy as np
from scipy.stats import gaussian_kde
import pandas as pd
import h5py
import matplotlib.pyplot as plt
import gc

from sklearn.utils.extmath import density

toolA_root = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261012_005148-v48_HPRF_Shorts_104D_1Dtune_PBprof\fxt-20261012_005148"
toolB_root = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261017_155800-v49_HPRF_Shorts_24D_1Dtune_CDF_check_Arizona_4p75nA\fxt-20261017_155800"

dies = ["c010r004", "c011r005", "c012r004", "c013r005"]

sample_size = 200000

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
    print(dfA.columns)

    #verify alignment once per die
    if not((dfA["Swath"].values == dfB["Swath"].values).all() and (dfA["blockIdx"].values == dfB["blockIdx"].values).all() and (dfA["localIdx"].values == dfB["localIdx"].values).all()):
        raise ValueError(f"Alignment mismatch between QKT406 and QKT524 for {die}")

    ############################################################
    ### SAMPLED PADS SCRIPT ###
    ###########################################################

    # idx= dfA.sample(n=min(sample_size, len(dfA)), random_state=42).index
    #
    # x = dfA.loc[idx, "GL_median"]
    # y = dfB.loc[idx, "GL_median"]
    #
    # #color scheme
    # # xy = np.vstack([x, y])
    # # density = gaussian_kde(xy)(xy)
    # # sort_idx = density.argsort()
    # # x = x.iloc[sort_idx]
    # # y = y.iloc[sort_idx]
    # # density = density[sort_idx]
    # ax.scatter(x, y, s=4, color = "blue", alpha=0.7, rasterized=True)
    # gmin = min(x.min(), y.min())
    # gmax = max(x.max(), y.max())
    # #ax.plot([gmin, gmax], [gmin, gmax], "k--", linewidth=1)
    # #linear fit
    # m, b = np.polyfit(x, y, 1)
    # x_fit = np.array([gmin, gmax])
    # y_fit = m*x_fit + b
    # ax.plot(x_fit, y_fit, color="darkorange", linewidth=2, label="linear fit")
    # r = x.corr(y)
    # ax.set_title(f"{die}\n" f"r = {r:.5f}\n" f"y = {m:4f}x + {b:.2f}\n" f"N = {len(x):,}", fontsize=10)
    #del x
    #del y

    # ###########################################################
    # ### HEX PLOT SCRIPT Ratio###
    # ###########################################################
    ratio = dfB["GL_median"]/dfA["GL_median"]
    hb = ax.hexbin(dfA["GL_median"], ratio, gridsize=200, bins="log", cmap="viridis", mincnt=1)
    # linear fit
    m, b = np.polyfit(dfA["GL_median"], ratio, 1)
    gmin = min(dfA["GL_median"].min(), dfB["GL_median"].min())
    xmin = dfA["GL_median"].min()
    xmax = dfA["GL_median"].max()
    gmax = max(dfA["GL_median"].max(), dfB["GL_median"].max())
    x_fit = np.array([xmin, xmax])
    y_fit = m * x_fit + b
    ax.plot(x_fit, y_fit, color="darkorange", linewidth=2, label="linear fit")
    r = dfA["GL_median"].corr(dfB["GL_median"])
    #ax.set_title(f"{die}\n" f"r = {r:.5f}\n" f"y = {m:4f}x + {b:.2f}", fontsize=10)
    mean_ratio = ratio.mean()
    std_ratio = ratio.std()
    ax.set_title(f"{die}\n" f"Mean Ratio = {mean_ratio:4f}\n" f"Ratio = {m:.4e}x + {b:.2f}", fontsize=10)
    ##############################################################
    del dfA
    del dfB
    gc.collect()
fig.supxlabel("QKT406 pad Median GL", fontsize=11)
fig.supylabel("QKT524/QKT406 GL ratio", fontsize=11)
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
#plt.savefig(r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261015_195701-v49_HPRF_Shorts_24D_1Dtune_CDF_check_Arizona\fxt-20261015_195701\QKT406_QKT524_4p75nA_ratio.png", dpi=300, bbox_inches="tight")
plt.show()