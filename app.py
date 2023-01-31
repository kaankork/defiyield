import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

df_rects = pd.read_csv('data/all_data.csv')

df_heatmap = pd.read_csv('data/heatmap.csv')
df_heatmap = df_heatmap.sort_values(["category", "issueType"], ascending=False)

x_categories = df_heatmap['issueType']
y_categories = df_heatmap['category']


options_issue_type = [
    'all_data'
    'abandoned', 
    'honeypot',
    'rugpull',
    'accesscontrol',
    'phishing',
    'flashloanattack',
    'reentrancy',
    'oracleissue',
    'other']

fig_issueType = px.histogram(df_rects, x="date", color="issueType", nbins=100)
fig_issueType.update_layout(
    title="Total Occurences per Issue Type",
    xaxis_title="",
    yaxis_title="Count",
    legend_title="Issue Types",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

fig_category = px.histogram(df_rects, x="date", color="category", nbins=100)
fig_category.update_layout(
    title="Total Occurences per Category",
    xaxis_title="",
    yaxis_title="Count",
    legend_title="Categories",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

fig_heatmap = go.Figure(data=go.Heatmap(
                        z=df_heatmap['fundsLost'],
                        x=x_categories,
                        y=y_categories,
                        hoverongaps = False,
                        colorscale='balance'))

fig_heatmap.layout.title = "Total Amount of Lost Funds ($)"
fig_heatmap.layout.height = 1200
fig_heatmap.layout.width = 1400

fig_heatmap.update_xaxes(side="top")
fig_heatmap.update_layout(xaxis=dict(showgrid=False),
              yaxis=dict(showgrid=False)
)

st.title("DeFiYield REKT DB Analytics Dashboard")
st.write("Created by Kaan Korkmaz.")

st.plotly_chart(fig_issueType, use_container_width=True)
st.plotly_chart(fig_category, use_container_width=True)
st.plotly_chart(fig_heatmap, use_container_width=True)