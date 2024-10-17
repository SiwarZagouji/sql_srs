# import ast
import os
import logging
import duckdb
import streamlit as st

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())



con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

st.write(
    """
# SQL SRS
Spaced Repetition System SQL Practice
"""
)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review",
        ("cross_joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme...",
    )

    st.write("You selected:", theme)
    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}' ").df().sort_values("last_reviewed").reset_index()
    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
    solution_df = con.execute(answer).df()



st.header("Enter your code")
query = st.text_area(label="your SQL code here", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)
#
    if len(result.columns) != len(solution_df.columns):
        st.write("The number of columns is wrong")
    if result.shape[0] != solution_df.shape[0]:
        st.write("The number of rows is not the same")
    # try:
    #     result = result[solution_df.columns]
    #     st.dataframe(result.compare(solution_df))
    # except KeyError as e:
    #     st.write("Some columns are missing")
#
#
tab1, tab2 = st.tabs(["Tables", "Solution"])
#
with tab1:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        st.dataframe(con.execute(f"SELECT * FROM {table}"))


with tab2:
    st.write(answer)
