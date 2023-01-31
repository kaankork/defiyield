import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Add vertical scroll for radio.
st.markdown("""
    <style>
        .row-widget.stRadio {
            height: 800px;
            overflow-y: scroll;
            overflow-y: auto;
        }
    </style>
    """,
    unsafe_allow_html=True)

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
st.markdown("Created by [Kaan Korkmaz](https://www.linkedin.com/in/kaankorkmaz/). Source code: https://github.com/kaankork/defiyield")
st.write("Hints:")
st.write("1 - Classes on plots can be hidden/unhidden by clicking on the legend. Double-click will select one class and hide the others.")
st.write("2 - fundsLost column on tables can be sorted by clicking on the header.")
st.write("---")
st.markdown("## How does the total amount of lost funds for each ISSUE TYPE evolve over time?")
col1, col2, col3 = st.columns([0.25, 0.05, 0.7])
with col1: 
    st.write("Choose an issue type")
    issue_type_selection = st.radio(label="Choose an issue type", 
                                    label_visibility="collapsed",
                                    options=['Abandoned', 
                                             'Access Control', 
                                             'Flash Loan Attack', 
                                             'Honeypot',
                                             'Oracle Issue', 
                                             'Other', 
                                             'Phishing', 
                                             'Reentrancy', 
                                             'Rugpull'
                                            ])

df_groupby_date_issueType = pd.read_csv('data/grouped_by_date_issueType_sum_fundsLost.csv')
df_filtered = df_groupby_date_issueType[df_groupby_date_issueType["issueType"] == issue_type_selection].reset_index(drop=True)
fig_fundsLost_issueType = px.line(df_filtered, x="date", y="fundsLost")

with col3:
    st.plotly_chart(fig_fundsLost_issueType, use_container_width=True)
    cols=["date", "issueType", "fundsLost"]
    st.dataframe(df_filtered[cols], use_container_width=True)
    
st.write("---")
st.markdown("## How does the total amount of lost funds for each CATEGORY evolve over time?")
col1_, col2_, col3_ = st.columns([0.25, 0.05, 0.7])
with col1_: 
    st.write("Choose a category")
    category_selection = st.radio(label="Choose a category", 
                                  label_visibility='collapsed',
                                    options=[
                                            'Bridge',
                                            'Borrowing and Lending,Exchange (DEX),Stablecoin',
                                            'Borrowing and Lending,NFT',
                                            'Borrowing and Lending,CeFi',
                                            'Borrowing and Lending',
                                            'Borrowing and Lending,Other',
                                            'Borrowing and Lending,Stablecoin',
                                            'Bridge,Exchange (DEX)',
                                            'Borrowing and Lending,Exchange (DEX)',
                                            'CeFi,Other',
                                            'CeFi',
                                            'CeFi,Yield Aggregator',
                                            'Exchange (DEX),Token',
                                            'Exchange (DEX),Yield Aggregator',
                                            'Exchange (DEX),NFT',
                                            'Exchange (DEX)',
                                            'Exchange (DEX),NFT,Token',
                                            'Gaming / Metaverse,NFT',
                                            'Gaming / Metaverse,NFT,Token',
                                            'Gaming / Metaverse,Yield Aggregator',
                                            'Gaming / Metaverse,Token',
                                            'Gaming / Metaverse',
                                            'NFT,Token',
                                            'NFT,Other',
                                            'NFT',
                                            'Other',
                                            'Other,Token',
                                            'Other,Yield Aggregator',
                                            'Stablecoin',
                                            'Stablecoin,Yield Aggregator',
                                            'Token,Yield Aggregator',
                                            'Token',
                                            'Yield Aggregator'
                                            ])

df_groupby_date_category = pd.read_csv('data/grouped_by_date_category_sum_fundsLost.csv')
df_filtered_category = df_groupby_date_category[df_groupby_date_category["category"] == category_selection].reset_index(drop=True)
fig_fundsLost_category = px.line(df_filtered_category, x="date", y="fundsLost")

with col3_:
    st.plotly_chart(fig_fundsLost_category, use_container_width=True)
    cols=["date", "category", "fundsLost"]
    st.dataframe(df_filtered_category[cols], use_container_width=True)
    
st.write("---")
st.markdown("## How does occurency count of each CATEGORY evolve over time?")
st.plotly_chart(fig_issueType, use_container_width=True)
st.write("---")
st.markdown("## How does occurency count of each ISSUE TYPE evolve over time? ")
st.plotly_chart(fig_category, use_container_width=True)
st.write("---")
st.markdown("## Which issue types tend to be more frequent for each category? ")
st.plotly_chart(fig_heatmap, use_container_width=True)