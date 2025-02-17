
## Part 1
Run the function `part1` in `main.py` file under the project directory to benchmark CSV and parquet file types with 
scaling factors of 1, 10, and 100.
```python
part1(csv_file_path)
```
Benchmark data will be written to `stock-price-prediction/data/benchmark/benchmark_results.json`\
Here is the result:
```json
{
    "Scaling 1x": {
        "CSV": {
            "read_time": 0.36,
            "file_size": 28.21
        },
        "Parquet (snappy)": {
            "read_time": 0.04,
            "file_size": 10.15
        },
        "Parquet (gzip)": {
            "read_time": 0.03,
            "file_size": 8.06
        },
        "Parquet (brotli)": {
            "read_time": 0.03,
            "file_size": 7.76
        },
        "Parquet (zstd)": {
            "read_time": 0.03,
            "file_size": 8.09
        },
        "Parquet (lz4)": {
            "read_time": 0.02,
            "file_size": 9.45
        },
        "Parquet (none)": {
            "read_time": 0.02,
            "file_size": 12.73
        }
    },
    "Scaling 10x": {
        "CSV": {
            "read_time": 3.53,
            "file_size": 282.1
        },
        "Parquet (snappy)": {
            "read_time": 0.22,
            "file_size": 95.32
        },
        "Parquet (gzip)": {
            "read_time": 0.23,
            "file_size": 75.97
        },
        "Parquet (brotli)": {
            "read_time": 0.26,
            "file_size": 73.18
        },
        "Parquet (zstd)": {
            "read_time": 0.17,
            "file_size": 75.42
        },
        "Parquet (lz4)": {
            "read_time": 0.17,
            "file_size": 88.37
        },
        "Parquet (none)": {
            "read_time": 0.15,
            "file_size": 118.02
        }
    },
    "Scaling 100x": {
        "CSV": {
            "read_time": 84.74,
            "file_size": 2821.02
        },
        "Parquet (snappy)": {
            "read_time": 7.12,
            "file_size": 951.92
        },
        "Parquet (gzip)": {
            "read_time": 10.52,
            "file_size": 758.13
        },
        "Parquet (brotli)": {
            "read_time": 12.35,
            "file_size": 730.49
        },
        "Parquet (zstd)": {
            "read_time": 6.55,
            "file_size": 751.62
        },
        "Parquet (lz4)": {
            "read_time": 6.86,
            "file_size": 882.42
        },
        "Parquet (none)": {
            "read_time": 5.46,
            "file_size": 1178.44
        }
    }
}
```

### Conclusion:
For small datasets, CSV is a good choice because it is human-readable and easy to work with.
For large datasets, Parquet is a better choice because it is more efficient in terms of storage and read/write
performance especially when using compression. Out of the Parquet's compression types tested, zstd and gzip are good choices
for a balance between compression size and read/write performance.

## Part 2
Run the function `part2` in the `main.py` file to benchmark the performance of Pandas vs Polars and train stock price prediction models
```python
part2(csv_file_path)
```
Benchmark result:
```
Pandas processing time: 1.51s
Polars processing time: 0.39s
```
### Conclusion:
Polars performs significantly better in terms of running time compared to Pandas. However, if you are already
familiar with Pandas, it's better to stick with it unless your data is large and an improvement in running time
is critical for your application because it takes time to adapt to Polars' new syntax.

Model training result:
```
Linear Regression - MAE: 0.9810, RMSE: 2.3458, R2: 0.9997, MAPE: 0.0103
Gradient Boosting (XGBoost) - MAE: 3.8447, RMSE: 36.8855, R2: 0.9165, MAPE: 0.0142
```
### Conclusion
Linear Regression has better metrics with a higher R squared, a lower root mean squared error (RMSE), a lower mean 
absolute error (MAE), and a lower mean absolute percentage error (MAPE). Therefore, Linear Regression is chosen. The
prediction data used for the visualization dashboard is stored in `data/prediction` folder under the name 
`predicitons.csv`. This file will later be used by Streamlit to load the data for the price prediction dashboard. 

## Part 3
### Comparing Streamlit and Dash:
To run the dashboards, open a terminal, navigate to the project directory (under stock-price-prediction) and run 
the following commands:\
For Streamlit:
```
streamlit run part3/streamlit_benchmark_dashboard.py
```
For Dash:
```
python3 part3/dash_benchmark_dashboard.py
```

### Conclusion:
Both dashboard frameworks are viable solutions to data visualization and interactive dashboards but Streamlit is
easier to learn and use as you only need a few lines of code to get your dashboard up and running. Dash, on the
other hand, requires more setup. You need to define layouts using HTML components and callbacks, which makes it
more complex than Streamlit. However, Dash runs faster on large scales and gives you more control/customization
over your Dashboard. Therefore, it depends on particular use cases to choose right frameworks, for this
assignment, Streamlit wins because of its simplicity and fast setup.

To run the price prediction dashboard, stay in the same directory (the project directory) and run the following
command:
```
streamlit run part3/streamlit_price_prediction_dashboard.py
```