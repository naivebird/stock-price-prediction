import json
import zipfile
from os.path import dirname, join

from part1.load_data import benchmark_csv_vs_parquet
from part2.process_data import benchmark_pandas_vs_polars
from part2.train_models import train_stock_price_prediction_models

ZIP_FILE_PATH = join(dirname(__file__), "data/input/all_stocks_5yr.zip")
BENCHMARK_FILE_PATH = join(dirname(__file__), "data/benchmark/benchmark_results.json")
PREDICTION_FILE_PATH = join(dirname(__file__), "data/prediction/predictions.csv")


def unzip_data():
    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
        zip_ref.extractall(dirname(ZIP_FILE_PATH))
    return ZIP_FILE_PATH.replace(".zip", ".csv")


def write_benchmark_data(data):
    with open(BENCHMARK_FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def part1(file_path):
    benchmark_1x = benchmark_csv_vs_parquet(file_path=file_path,
                                            factor=1)

    benchmark_10x = benchmark_csv_vs_parquet(file_path=file_path,
                                             factor=10)

    benchmark_100x = benchmark_csv_vs_parquet(file_path=file_path,
                                              factor=100)

    benchmark_data = {
        "Scaling 1x": benchmark_1x,
        "Scaling 10x": benchmark_10x,
        "Scaling 100x": benchmark_100x
    }

    write_benchmark_data(benchmark_data)


def part2(file_path):
    df = benchmark_pandas_vs_polars(file_path)
    train_stock_price_prediction_models(df, PREDICTION_FILE_PATH)


if __name__ == '__main__':
    csv_file_path = unzip_data()

    part1(csv_file_path)

    part2(csv_file_path)

