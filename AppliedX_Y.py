import pandas as pd
import matplotlib.pyplot as plt

scan1 = r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20260927_145202-V72_144D_137S_Tuned_new\c001r011\c001r011_Registration.log"
scan2 = r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20260928_174944-V69_144D_138S_Tuned\c001r011\c001r011_Registration.log"
scan3 = r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20261003_023038-V72_144D_137S_Tuned_TRIM\c001r011\c001r011_Registration.log"
scan4 = r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20261004_052616-V72_144D_137S_Tuned_TRIM\c001r011\c001r011_Registration.log"
scan5 = r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20261022_160219-V69_144D_138S_Tuned\c005r017\c005r017_Registration.log"
scan6 = r"N:\eProbe_Output\Recipes_Data\X80C\EMR\tst-20261028_164630-V69_144D_138S_150DT_Tuned\c005r017\c005r017_Registration.log"

df1 = pd.read_csv(scan1, sep='\t')
df2 = pd.read_csv(scan2, sep='\t')
df3 = pd.read_csv(scan3, sep='\t')
df4 = pd.read_csv(scan4, sep='\t')
df5 = pd.read_csv(scan5, sep='\t')
df6 = pd.read_csv(scan6, sep='\t')
#print(df.head())
# df1 = df1[df1["Type"] == 'reg']
# df2 = df2[df2["Type"] == 'reg']
# df3 = df3[df3["Type"] == 'reg']
# df4 = df4[df4["Type"] == 'reg']
df5 = df5[df5["Type"] == 'reg']
df6 = df6[df6["Type"] == 'reg']
df5 = df5.sort_values(by='Global_ID').reset_index(drop=True)
df6 = df6.sort_values(by='Global_ID').reset_index(drop=True)


fig, axs = plt.subplots(1, 2, figsize=(12, 4))
# df1.plot(x="Global_ID", y=["AppliedX", "AppliedY"], ax=axs[0,0], title="20260927_145202_DT100", xlim=(0,120000), ylim=(-2500,2500))
# df2.plot(x="Global_ID", y=["AppliedX", "AppliedY"], ax=axs[0,1], title="20260928_174944_DT200",xlim=(0,120000), ylim=(-2500,2500))
# df3.plot(x="Global_ID", y=["AppliedX", "AppliedY"], ax=axs[0,2], title="20261003_023038_DT100",xlim=(0,120000), ylim=(-2500,2500))
# df4.plot(x="Global_ID", y=["AppliedX", "AppliedY"], ax=axs[1,0], title="20261004_052616_DT100",xlim=(0,120000), ylim=(-2500,2500))
df5.plot(x="Global_ID", y=["AppliedX", "AppliedY"], ax=axs[0], title="DT = 200 ns",xlim=(0,120000), ylim=(-2500,2500))
df6.plot(x="Global_ID", y=["AppliedX", "AppliedY"], ax=axs[1], title="DT = 150 ns",xlim=(0,120000), ylim=(-2500,2500))
plt.xlabel("Global_ID")
plt.ylabel("Applied X/AppliedY")
plt.show()
fig, axs = plt.subplots(1, 2, figsize=(12, 4))
df5.plot(x="Global_ID", y=["LocX", "LocY"], ax=axs[0], title="DT = 200 ns")
df6.plot(x="Global_ID", y=["LocX", "LocY"], ax=axs[1], title="DT = 150 ns")
#plt.ylabel("Applied X/AppliedY")
plt.ylabel("LocX/LocY")
plt.xlabel("Global_ID")
plt.tight_layout()
plt.show()
