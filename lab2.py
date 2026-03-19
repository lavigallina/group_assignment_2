import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random

# Load dataset
df = pd.read_csv("flights-airport.csv")

st.title("Flight Traffic Analysis (A/B Testing)")

# Business question
st.subheader("Business Question:")
st.write("Which airports handle the highest flight traffic, and how is traffic distributed across routes?")

# Dataset preview
if st.checkbox("Show dataset preview"):
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

# Column selection
st.subheader("Select Variables for Analysis")
category_col = st.selectbox("Category (e.g., origin airport)", df.columns)
subcategory_col = st.selectbox("Sub-category (e.g., destination airport)", df.columns)
value_col = st.selectbox("Value (numeric, e.g., count of flights)", df.select_dtypes(include='number').columns)
color_col = st.selectbox("Optional color by (categorical)", [None] + list(df.select_dtypes(include='object').columns))

# Slider for top N
top_n = st.slider("Select top N airports/routes to display", min_value=5, max_value=20, value=10)

# Checkbox for showing raw filtered data
show_data = st.checkbox("Show data behind the chart")

# Check numeric
if not pd.api.types.is_numeric_dtype(df[value_col]):
    st.error("Please select a numeric column for the value.")
    st.stop()

# Button to show chart
if st.button("Show me a chart"):

    # Randomly choose which chart to show
    chart_type = random.choice(["A", "B"])
    st.session_state.chart_type = chart_type

    if chart_type == "A":
        # Chart A: Scatter plot (flight routes)
        st.write("### Chart A: Flight Routes Scatter Plot")

        # Filter top airports for clarity
        top_airports = df.groupby(category_col)[value_col].sum().sort_values(ascending=False).head(top_n).index
        df_filtered = df[df[category_col].isin(top_airports)]

        fig, ax = plt.subplots(figsize=(12,6))
        sns.scatterplot(
            data=df_filtered,
            x=category_col,
            y=subcategory_col,
            size=value_col,
            sizes=(50, 500),
            hue=color_col if color_col else None,
            alpha=0.7,
            ax=ax,
            palette="Set2"
        )
        plt.xticks(rotation=45)
        ax.set_xlabel(category_col)
        ax.set_ylabel(subcategory_col)
        if color_col:
            ax.legend(title=color_col, bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

        if show_data:
            st.subheader("Data Behind Chart A")
            st.dataframe(df_filtered.sort_values(by=value_col, ascending=False).head(top_n*3))

    else:
        # Chart B: Bar chart (top airports)
        st.write("### Chart B: Top Airports by Flight Count")
        top_airports = df.groupby(category_col)[value_col].sum().sort_values(ascending=False).head(top_n).reset_index()

        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(data=top_airports, x=category_col, y=value_col, ax=ax, palette="Blues_d")
        plt.xticks(rotation=45)
        ax.set_ylabel(f"{value_col} (flights)")
        st.pyplot(fig)

        if show_data:
            st.subheader("Data Behind Chart B")
            st.dataframe(top_airports)

# Additional widgets ideas:
st.sidebar.header("Additional Options")
st.sidebar.write("Customize your view:")
st.sidebar.slider("Adjust maximum bubble size in Chart A", min_value=50, max_value=800, value=500)

