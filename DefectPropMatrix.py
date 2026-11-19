import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib.colors import ListedColormap

QKT404= r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20260824_102320-V67_144D_136S_Tuned_D618E1Q0_220\fxt-20260824_102320\Anl-20260824_102321\ReviewInspection\Verified_Review_Plan.csv"
QKT406= r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20260825_163837-V67_144D_136S_Tuned_default_Slot04_QKT406\ReviewInspection\Verified_Review_Plan.csv"
stg0_QKT406 = r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20260825_163837-V67_144D_136S_Tuned\fxt-20260825_163837\Anl-20260825_163839\Rev-20260825_184913\outliers_dir\stg0_Total_outliers_read_from_partial_review_files.csv"
stg9_QKT406 = r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20260825_163837-V67_144D_136S_Tuned\fxt-20260825_163837\Anl-20260825_163839\Rev-20260825_184913\outliers_dir\stg9_OutlierCnt_after_Cluster_Removal.csv"
OS_Prefltr = r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20260825_163837-V67_144D_136S_Tuned\fxt-20260825_163837\Anl-20260825_163839\Rev-20260825_184913\outliers_dir\OS_preFilter.csv"

df1 = pd.read_csv(QKT404, skiprows=17, header=0)
df2 = pd.read_csv(QKT406, skiprows=16, header=0)
df_stg0 = pd.read_csv(stg0_QKT406, header=0)
df_stg9 = pd.read_csv(stg9_QKT406, header=0)
df_OSPF = pd.read_csv(OS_Prefltr, header=0)

dfs = [ ("QKT406_OS_PreFilter",df_OSPF),("QKT406_Stg0", df_stg0), ("QKT406_stg9", df_stg9), ("QKT406_VRP", df2)]

cols = ["Die_Column", "Die_Row", "blockIdx", "localIdx"]

Sur_Mat = df1[cols].copy()

for name, df in dfs:
    Sur_Mat[name] = (pd.MultiIndex.from_frame(Sur_Mat[cols]).isin(pd.MultiIndex.from_frame(df[cols])))

print(Sur_Mat.head(5))
#Sur_Mat.to_csv(r"N:\Users\4Shashi\Defect_Propagation_Of_QKT406_At_Multiple_Stages_WRT_QKT404VRP_1.csv")

## HEAT MAP ##
stage_cols = [name for name, df in dfs]
# Plot_Mat = Sur_Mat[Sur_Mat[stage_cols.any(axis=1)]].copy()
# Plot_Mat["Defects"] = Plot_Mat[cols].astype(str).agg("_".join,axis=1)
#
# fig = px.imshow(Plot_Mat.set_index("Defects")[stage_cols], color_continuous_scale=["red", "green"], aspect="auto")
# fig.update_layout(title="Defect Propagation Of QKT406", xaxis_title = "Stage", yaxis_title = "Defects")
# fig.show()

fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(Sur_Mat[stage_cols], aspect="auto", cmap=ListedColormap(["red","green"]), interpolation="nearest")

ax.set_xticks(range(len(stage_cols)))
ax.set_xticklabels(stage_cols, rotation=45, ha="right")

ax.set_yticks([])
ax.set_xlabel("Stage")
ax.set_ylabel("Defects")
ax.set_title("Defect Propagation Of QKT406")

plt.tight_layout()
plt.show()