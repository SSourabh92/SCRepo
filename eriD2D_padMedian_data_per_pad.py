import os.path
import re
from pathlib import Path
import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt

cal_dirs = ["Cal-L1_202005.769t33", "Cal-L1_202011.310t23", "Cal-L1_202011.878-t3", "Cal-L1_202007.245t43", "Cal-L1_202011.765t13"]
target_die = "c010r004"
#root_dir = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261012_005148-v48_HPRF_Shorts_104D_1Dtune_PBprof\fxt-20261012_005148\Anl-20261012_200026\Cal-L1_200326.678t41\SCANLINE_DIFF\output_files"
base_dir = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261012_005148-v48_HPRF_Shorts_104D_1Dtune_PBprof\fxt-20261012_005148\Anl-20261012_200026"
records = []
for cal_dir in cal_dirs:
    root_dir = (Path(base_dir)/cal_dir/"SCANLINE_DIFF"/"output_files")
    print(f"Processing {cal_dir}")
    for h5_file in Path(root_dir).rglob("*.h5"):
        #print(f"Processing {h5_file.name}")
        parts = h5_file.stem.split(".")
        die_id = next((p for p in parts if re.match(r"c\d+r\d+", p)), None)
        if die_id.lower() != target_die.lower():
            continue
        swath_id = parts[-1]
        with h5py.File(h5_file, "r") as f:
            die_group = list(f.keys())[0]
            for swath_id, swath_grp in f[die_group].items():
                for block_idx, ds in swath_grp.items():
                    #for dataset_name, ds in block_grp.items():
                    if not isinstance(ds, h5py.Dataset):
                        continue
                    arr = ds[:]
                    df_tmp = pd.DataFrame({"DieID": die_id, "SwathID": swath_id, "blockIdx": int(block_idx), "localIdx": arr["localIdx"], "padMedian": arr["padMedian"], "erid2d": arr["eri_d2d_diff"]})
                    records.append(df_tmp)

if not records:
    raise Exception("No records found")
master_df = pd.concat(records, ignore_index=True)
print(master_df.head(3))
master_df = master_df.to_parquet(r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261012_005148-v48_HPRF_Shorts_104D_1Dtune_PBprof\fxt-20261012_005148\Anl-20261012_200026\c010r004.parquet", index=False)
print(master_df.shape)

