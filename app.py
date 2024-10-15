import streamlit as st
import pandas as pd
import duckdb

st.write("""
# SQL SRS
Spaced Repetition System SQL Practice
""")

option = st.selectbox(
    "What would you like to review",
    ("Joins", "GroupBy", "Windows Functions"),
    index=None,
    placeholder="Select a theme...",
)

st.write("You selected:", option)

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)


input_text = st.text_input(label="entrez votre input")
st.write(input_text)
result = duckdb.query(input_text)
st.dataframe(df)
st.dataframe(result)

