import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output

from dashboard_utils import load_benchmark_data

df = load_benchmark_data()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Benchmark Data Dashboard"),
    html.H3("Full Benchmark Data"),
    html.Div(dash.dash_table.DataTable(
        id="data-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        page_size=10,
    )),
    html.H3("Grouped Bar Chart: Read Time by Scaling Factor"),
    dcc.Graph(id="read-time-chart"),
    html.H3("Grouped Bar Chart: File Size by Scaling Factor"),
    dcc.Graph(id="file-size-chart"),
])


@app.callback(
    [Output("read-time-chart", "figure"), Output("file-size-chart", "figure")],
    [Input("data-table", "data")]
)
def update_charts(data):
    df = pd.DataFrame(data)

    read_time_fig = px.bar(
        df,
        x="File Type",
        y="read_time",
        color="Scaling Factor",
        barmode="group",
        title="Read Time Comparison by Scaling Factor",
        labels={"read_time": "Read Time (s)", "Compression Type": "Compression Type"},
    )

    file_size_fig = px.bar(
        df,
        x="File Type",
        y="file_size",
        color="Scaling Factor",
        barmode="group",
        title="File Size Comparison by Scaling Factor",
        labels={"file_size": "File Size (MB)", "Compression Type": "Compression Type"},
    )

    return read_time_fig, file_size_fig


if __name__ == "__main__":
    app.run(debug=True)
