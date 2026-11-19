import pandas as pd
import matplotlib.pyplot as plt

QKT404= r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20260824_102320-V67_144D_136S_Tuned_D618E1Q0_220\fxt-20260824_102320\Anl-20260824_102321\ReviewInspection\Verified_Review_Plan.csv"
QKT406= r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20260825_163837-V67_144D_136S_Tuned_default_Slot04_QKT406\ReviewInspection\Verified_Review_Plan.csv"

df1 = pd.read_csv(QKT404, skiprows=17, header=0)
df2 = pd.read_csv(QKT406, skiprows=16, header=0)

cols = ["Die_Column", "Die_Row", "blockIdx", "localIdx"]

df1["Status"] = (pd.MultiIndex.from_frame(df1[cols]).isin(pd.MultiIndex.from_frame(df2[cols])))
df2["Status"] = (pd.MultiIndex.from_frame(df2[cols]).isin(pd.MultiIndex.from_frame(df1[cols])))
df1["Status"] = df1["Status"].map({True: "Common", False: "Not Found"})
df2["Status"] = df2["Status"].map({True: "Common", False: "Not Found"})

df1.to_csv(r"N:\Users\4Shashi\QKT404_Defects_in_QKT406.csv")
df2.to_csv(r"N:\Users\4Shashi\QKT406_Defects_in_QKT404.csv")

#common_review_true_df1 = df1[(df1["Review"] == True) & (df1["Status"] == "Common")]
common_review_true_df1 = df1[(df1["Status"] == "Common")]
df_common_elements = df1[(df1["Status"] == "Common")].copy()
common_review_true_df2 = df2[(df2["Status"] == "Common")]
#common_review_true_df2 = df2[(df2["Review"] == True) & (df2["Status"] == "Common")]
df_common_elements.to_csv(r"N:\Users\4Shashi\Common_defects_between_Tools.csv")
#print(len(common_review_true_df1))
#print(len(common_review_true_df2))
#print(common_review_true_df1)
#print(df_common_elements.columns)
#plt.scatter(df_common_elements["eri_d2d_diff"], df_common_elements["outlierStrength_tail4shorts"])
# plt.scatter(df1[df1["Status"] == "Common"]["eri_d2d_diff"], df2[df2["Status"] == "Common"]["eri_d2d_diff"], s=40, c='r')
# plt.ylabel('erid2d_QKT524', fontsize = 12)
# plt.xlabel('erid2d_QKT404', fontsize = 12)
# plt.xticks(fontsize=10)
# plt.yticks(fontsize=10)
# plt.show()