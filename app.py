import streamlit as st
import pandas as pd
import duckdb

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

st.write("Hello World")
input_text = st.text_input(label="entrez votre input")
st.write(input_text)
result = duckdb.query(input_text)
st.dataframe(df)
st.dataframe(result)

