import re

import pandas as pd
temp_df = pd.read_csv(r"N:\Users\4Shashi\output.csv", index_col=0, on_bad_lines = 'skip')
df_reset = temp_df.reset_index()
x = df_reset[df_reset.iloc[:,0]=='-- CSF --'].index[0]
df = df_reset.iloc[x+1:,0]
df_fil = df[df.iloc[:].str.extract(r'(\d+)D')[0].astype(float) >= 32]
df_filter = df_fil.astype(str).str.rstrip().str.endswith('D')
df_result = df_fil[df_filter]
df_result.to_csv(r"N:\Users\4Shashi\filtered_output.csv", index=False)

#Let's create a  different column which will have full path
base_path = r"N:\eProbe_Setup\Recipe-Repo\JobRecipe"
df_fullpath = (base_path + "\\" + df_result.str.split("_").str[0] + "\\" + df_result.str.split("_").str[1:-3].str.join("_")+ "\\" + df_result.str.strip()+".xml")
df_fullpath.to_csv(r"N:\Users\4Shashi\fullpath.csv", index=False)
#Now loop through each file and then loop inside the file to go to specific line and print:
Recipe_Csv_list = []
Yaml_list = []

for path in df_fullpath:
    try:
        with open(path, encoding='utf-8') as f:
            lines = f.readlines()
            Recipe_Csv_list.append(re.search(r"<Value>(.*?)</Value>", lines[127]).group(1))
            Yaml_list.append(re.search(r"<Value>(.*?)</Value>", lines[243]).group(1))
            #print(f"\nFile: {path}")
            #print("Line 128:", lines[127].strip())
            #print("Line 244:", lines[243].strip())
    except Exception as e:
        #print(f"Error with {path}: {e}")
        break
print(Recipe_Csv_list)
#print(Yaml_list[0])
for file in Recipe_Csv_list:
    with open(file, 'r') as f:
        last_line = f.readlines()[-1].strip()
    print(f"{file}-> {last_line}")