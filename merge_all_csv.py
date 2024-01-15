import os
import pandas as pd

path = "./csvovi"


csvFilesPath = []
for dir in os.listdir(path):
    pathDir = f"{path}/{dir}"
    dirContent = os.listdir(pathDir)
    for item in dirContent:
        if item.startswith("listing_links"):
            csvFilesPath.append(f"{pathDir}/{item}")


df_list = []
for csvFilePath in csvFilesPath:
    try:
        df = pd.read_csv(csvFilePath)
        df_list.append(df)
    except Exception as e:
        print(f"Could not read file {csvFilePath} because of error: {e}")

big_df = pd.concat(df_list, ignore_index=True)

big_df.to_csv(os.path.join("./", "merged_data.csv"), index=False)