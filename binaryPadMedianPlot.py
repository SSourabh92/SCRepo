import os.path

import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt

h5_file = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261012_005148-v48_HPRF_Shorts_104D_1Dtune_PBprof\v48_HPRF_Shorts_104D_1Dtune_PBprof.h5"
recipe_root = r"N:\eProbe_Output\Recipes_Data\X78D\VC\tst-20261017_155800-v49_HPRF_Shorts_24D_1Dtune_CDF_check_Arizona_4p75nA\fxt-20261017_155800"
dies = ["c010r004", "c011r005", "c012r004", "c013r005"]

# Loading the pad list in the sequence used by FPGA:
def create_die_parquet(die):
    die_folder = os.path.join(recipe_root, die)
    df_list=[]
    with h5py.File(h5_file, "r") as f:
        for swath in f["Swaths"].keys():
            #read the swath dataset table
            swath_table = f[f"Swaths/{swath}"][:]
            median_file = os.path.join(die_folder, swath, "median.bin")
            if not os.path.exists(median_file):
                print(f"Missing: {median_file}")
                continue
            median_bin = np.fromfile(median_file, dtype=np.uint16)
            df = pd.DataFrame({"blockIdx": swath_table['blockIdx'], "localIdx": swath_table['localIdx'], "GL_median": median_bin})
            df['Swath'] = swath
            #memory optimization
            df["blockIdx"] = df["blockIdx"].astype("uint32")
            df["localIdx"] = df["localIdx"].astype("uint16")
            df["GL_median"] = df["GL_median"].astype("uint16")
            df_list.append(df)
    df_die = pd.concat(df_list, ignore_index=True)
    df_die.to_parquet(os.path.join(die_folder, f"{die}.parquet"), index=False)
    print(f"die path = {os.path.join(die_folder, f'{die}.parquet')}")
    print(f"Shape = {df_die.shape}")

###########################
##MAIN LOOP##
###########################

for die in dies:
    create_die_parquet(die)
print("All Done")
