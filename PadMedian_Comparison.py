import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import xlabel

RP1 = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261015_195701-v49_HPRF_Shorts_24D_1Dtune_CDF_check_Arizona\fxt-20261015_195701\Anl-20261015_195701\Rev-20261015_201428\outliers_dir\bidx_stats.csv"
RP2 = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261012_005148-v48_HPRF_Shorts_104D_1Dtune_PBprof\fxt-20261012_005148\Anl-20261012_200026\Rev-20261012_204804\outliers_dir\bidx_stats.csv"

#Reading the .csv review_plan
df1 = pd.read_csv(RP1)
df2 = pd.read_csv(RP2)

df1 = df1.rename(columns={'padMedian_percentile_50': 'padMedian_percentile_50_QKT406', 'padMedian_percentile_95': 'padMedian_percentile_95_QKT406', 'padMedian_percentile_5': 'padMedian_percentile_05_QKT406'})
df2 = df2.rename(columns={'padMedian_percentile_50': 'padMedian_percentile_50_QKT524', 'padMedian_percentile_95': 'padMedian_percentile_95_QKT524', 'padMedian_percentile_5': 'padMedian_percentile_05_QKT524'})

#inner merge on dieIdx and blockIdx

merged = pd.merge(df1, df2, on=['dieIdx', 'blockIdx'], how='inner')
merged = merged.rename(columns={'swathIdx_x':'swathIdx'})
print(f"Common rows: {len(merged)}")
print(merged.columns.tolist())
#Scatter plot:
#merged.plot(x="padMedian_percentile_50_QKT406", y='padMedian_percentile_50_QKT524', ax=axs[0], kind='scatter', color = 'darkorange', alpha = 0.5, title="QKT524 vs QKT406: padMedian_p50")
colors = pd.factorize(merged['dieIdx'])[0]
plt.scatter(merged['padMedian_percentile_50_QKT406'], merged['padMedian_percentile_50_QKT524'], c=colors, cmap='turbo',s=10,alpha=0.6)
plt.xlabel('padMedian_percentile_50_QKT406')
plt.ylabel('padMedian_percentile_50_QKT524')
#Linear fitting:
# m, b = np.polyfit(merged['padMedian_percentile_50_QKT406'], merged['padMedian_percentile_50_QKT524'], 1 )
# r = np.corrcoef(merged['padMedian_percentile_50_QKT406'], merged['padMedian_percentile_50_QKT524'])[0,1]
xfit = np.linspace(merged['padMedian_percentile_50_QKT406'].min(), merged['padMedian_percentile_50_QKT406'].max(), 100)
yfit = np.linspace(merged['padMedian_percentile_50_QKT524'].min(), merged['padMedian_percentile_50_QKT524'].max(), 100)

#axs[0].plot(xfit, m*xfit+b, color='r', linewidth=2, label=f'Fit: y={m:.3f}x+{b:.1f}\nCorrelation(r)={r:.4f}')
plt.plot(xfit, yfit, color='b', linewidth=2, label='straight line')
plt.legend()
plt.show()
#Swath wise plot and diewise color:
swaths = sorted(merged['swathIdx'].unique())
ncols = 4
nrows = int(np.ceil(len(swaths) / ncols))
fig, axs = plt.subplots(nrows, ncols, figsize=(3*ncols,3*nrows))
axs = np.array(axs).flatten()
for ax, swath in zip(axs, swaths):
    temp = merged[merged['swathIdx'] == swath]
    colors = pd.factorize(temp['dieIdx'])[0]
    ax.scatter(temp['padMedian_percentile_50_QKT406'], temp['padMedian_percentile_50_QKT524'], c=colors, cmap='tab20',s=10, alpha=0.6)
    r = temp['padMedian_percentile_50_QKT406'].corr(temp['padMedian_percentile_50_QKT524'])
    ax.set_title(f'{swath} (r={r:.4f})')
    ax.set_xlabel('QKT406 P50')
    ax.set_ylabel('QKT524 P50')
    ax.grid(alpha=0.5)
    ax.plot(ax.get_xlim(), ax.get_ylim(), color='k', linestyle='dashed', linewidth=0.5, alpha=0.7)
plt.tight_layout()
plt.show()

#P95P05
# merged['spread_QKT406'] = (merged['padMedian_percentile_95_QKT406'] - merged['padMedian_percentile_05_QKT406'])
# merged['spread_QKT524'] = (merged['padMedian_percentile_95_QKT524'] - merged['padMedian_percentile_05_QKT524'])
# merged.plot(x='spread_QKT406', y='spread_QKT524', ax=axs[1], kind='scatter', title="QKT524 vs QKT406: padMedian_p95-p05")
# plt.axis('equal')
# plt.show()