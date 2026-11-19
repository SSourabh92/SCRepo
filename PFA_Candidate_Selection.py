import pandas as pd

#Importing the review_plan.csv files:
RP1 = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20260609_053221-v48_HPRF_Shorts_45D_1Dtune_GD_From_QKT404\fxt-20260609_053221\Anl-20260609_053221\Rev-20260609_061425\review_plan.csv"
RP2 = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20260921_121059-v48_HPRF_Shorts_45D_1Dtune_GD\fxt-20260921_121059\Anl-20260921_121100\Rev-20260921_125053\review_plan.csv"
RP3 = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20260921_125848-v48_HPRF_Shorts_45D_1Dtune_GD\fxt-20260921_125848\Anl-20260921_125848\Rev-20260921_133846\review_plan.csv"
RP4 = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20260921_134642-v48_HPRF_Shorts_45D_1Dtune_GD\fxt-20260921_134642\Anl-20260921_134643\Rev-20260921_142643\review_plan.csv"

#Reading the .csv review_plan
df1 = pd.read_csv(RP1, skiprows=17)
df2 = pd.read_csv(RP2, skiprows=17)
df3 = pd.read_csv(RP3, skiprows=17)
df4 = pd.read_csv(RP4, skiprows=17)

#This block identifies which defect came from which source:
df1["Source"] = "QKT404"
df2["Source"] = "QKT524 1st scan"
df3["Source"] = "QKT524 2nd scan"
df4["Source"] = "QKT524 3rd scan"

#Applying ERI/OS filter to each file/Dataframe:
df1 = df1[(df1["eri_d2d_diff"] >= 1045) & (df1["outlierStrength_tail4shorts"] >= 800) & (df1["Review"] == True)]
df2 = df2[(df2["eri_d2d_diff"] >= 1200) & (df2["outlierStrength_tail4shorts"] >= 1080)]
df3 = df3[(df3["eri_d2d_diff"] >= 1200) & (df3["outlierStrength_tail4shorts"] >= 1080)]
df4 = df4[(df4["eri_d2d_diff"] >= 1200) & (df4["outlierStrength_tail4shorts"] >= 1080)]
print(f"DF1 Shape = {df1.shape}")
print(f"DF2 Shape = {df2.shape}")
print(f"DF3 Shape = {df3.shape}")
print(f"DF4 Shape = {df4.shape}")

#Creating merged dataframe and unique merged review plan:
mergeddf = pd.concat([df1, df2, df3, df4], ignore_index=True)
mergeddf_3scans = pd.concat([df2, df3, df4], ignore_index=True)
duplicate_columns = ["Die_Column", "Die_Row", "blockIdx", "localIdx"]

#This defines the all sources in the merged duplicate defects:
mergeddf["Source"] = mergeddf.groupby(duplicate_columns)["Source"].transform(lambda x: ", ".join(x.unique()))
mergeddf_3scans["Source"] = mergeddf_3scans.groupby(duplicate_columns)["Source"].transform(lambda x: ", ".join(x.unique()))

unique_df = mergeddf.drop_duplicates(subset=duplicate_columns, keep="first").reset_index(drop=True)
duplicate_df = mergeddf[mergeddf.duplicated(subset=duplicate_columns, keep=False)]
duplicate_df_across3scans = mergeddf_3scans[mergeddf_3scans.duplicated(subset=duplicate_columns, keep=False)]
unique_duplicate_df = duplicate_df.drop_duplicates(subset=duplicate_columns, keep="first")

#unique_duplicate_df.to_csv(r"N:\Users\Shashi\Merged_Review_Plan\PFA_Candidates_404.csv", index=False)
#unique_df.to_csv(r"N:\Users\Shashi\Merged_Review_Plan\Merged_unique_review_plan_404.csv", index=False)
#mergeddf.to_csv(r"N:\Users\Shashi\Merged_Review_Plan\non_unique_merged_review_plan_404.csv", index=False)
#duplicate_df.to_csv("N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20260401_135532-v15_P180_HVT_RVT_61D_1Dtune_GD\duplicate_df.csv", index=False)

print("No. of overall unique elements in final review plan = ", len(unique_df))
#print("No. of overall duplicate elements = ", len(duplicate_df))
#print("No. of unique duplicates = ", len(unique_duplicate_df))
#print("No. of elements in merged review plan = ", len(mergeddf))
print("Repeatability across all 4 scans = ", len(duplicate_df)/len(mergeddf)*100, "%")
print("Repeatability across 3 scans on same tool = ", len(duplicate_df_across3scans)/len(mergeddf_3scans)*100, "%")