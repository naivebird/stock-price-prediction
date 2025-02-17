import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from part3.dashboard_utils import load_benchmark_data

df = load_benchmark_data()

st.title("Benchmark Data Dashboard")

st.subheader("Full Benchmark Data")
st.dataframe(df)

st.subheader("Grouped Bar Chart: Read Time by Scaling Factor")
fig, ax = plt.subplots(figsize=(12, 6))

file_types = df["File Type"].unique()
scaling_factors = df["Scaling Factor"].unique()

bar_width = 0.2
x = np.arange(len(file_types))

for i, scaling_factor in enumerate(scaling_factors):
    read_times = df[df["Scaling Factor"] == scaling_factor]["read_time"]
    ax.bar(x + i * bar_width, read_times, width=bar_width, label=scaling_factor)

ax.set_xlabel("File Type")
ax.set_ylabel("Read Time (s)")
ax.set_title("Read Time Comparison by Scaling Factor")
ax.set_xticks(x + bar_width * (len(scaling_factors) - 1) / 2)
ax.set_xticklabels(file_types, rotation=45)
ax.legend(title="Scaling Factor")

st.pyplot(fig)

st.subheader("Grouped Bar Chart: File Size by Scaling Factor")
fig, ax = plt.subplots(figsize=(12, 6))

for i, scaling_factor in enumerate(scaling_factors):
    file_sizes = df[df["Scaling Factor"] == scaling_factor]["file_size"]
    ax.bar(x + i * bar_width, file_sizes, width=bar_width, label=scaling_factor)

ax.set_xlabel("File Type")
ax.set_ylabel("File Size (MB)")
ax.set_title("File Size Comparison by Scaling Factor")
ax.set_xticks(x + bar_width * (len(scaling_factors) - 1) / 2)
ax.set_xticklabels(file_types, rotation=45)
ax.legend(title="Scaling Factor")

st.pyplot(fig)
