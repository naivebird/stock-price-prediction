import json

import pandas as pd

from main import BENCHMARK_FILE_PATH


def load_benchmark_data():
    with open(BENCHMARK_FILE_PATH, "r") as file:
        benchmark_data = json.load(file)

    df_list = []
    for scaling_factor, data in benchmark_data.items():
        temp_df = pd.DataFrame(data).T.reset_index()
        temp_df["Scaling Factor"] = scaling_factor
        df_list.append(temp_df)

    df = pd.concat(df_list)
    return df.rename(columns={"index": "File Type"})
