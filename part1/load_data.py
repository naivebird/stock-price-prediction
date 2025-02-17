import os
import time

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def scale_table(table, factor):
    return pa.concat_tables([table] * factor)


def scale_dataframe(df, factor):
    return pd.concat([df] * factor, ignore_index=True)


def prepare_csv_file(file_path, factor):
    csv_file_path = file_path.replace(".csv", f"_{factor}x.csv")
    df = pd.read_csv(file_path)
    df = scale_dataframe(df, factor)
    df.to_csv(csv_file_path, index=False)
    return csv_file_path


def get_parquet_table(file_path):
    df = pd.read_csv(file_path)
    return pa.Table.from_pandas(df)


def benchmark_csv_vs_parquet(factor, file_path):
    print(f"Scaling factor: {factor}")

    result = {}

    csv_file_path = prepare_csv_file(file_path, factor)

    start = time.time()
    pd.read_csv(csv_file_path)
    end = time.time() - start
    size = os.path.getsize(csv_file_path) / 1024 / 1024
    print(f"CSV read time: \t\t\t\t\t\t\t\t{end:.2f}s, \tfile size: {size:.2f} MB")

    result["CSV"] = {"read_time": round(end, 2), "file_size": round(size, 2)}
    os.remove(csv_file_path)

    table = get_parquet_table(file_path)

    parquet_file_path = file_path.replace(".csv", ".parquet")
    compression_types = ["snappy", "gzip", "brotli", "zstd", "lz4", "none"]
    for compression_type in compression_types:
        pq.write_table(scale_table(table, factor), parquet_file_path, compression=compression_type)

        start = time.time()
        pq.read_table(parquet_file_path)
        end = time.time() - start
        size = os.path.getsize(parquet_file_path) / 1024 / 1024
        print(
            f"Parquet with {compression_type} compression read time: \t{end:.2f}s, \tfile size: {size:.2f} MB")
        result[f"Parquet ({compression_type})"] = {"read_time": round(end, 2), "file_size": round(size, 2)}
        os.remove(parquet_file_path)

    return result
