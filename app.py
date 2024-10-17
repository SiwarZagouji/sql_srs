# import ast
import os
import logging
import duckdb
import streamlit as st
from datetime import date, timedelta

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

def check_user_solution(user_query : str) -> None:
    """
    checks the user SQL query if it is correct by:
    1. checking the columns
    2. checking the rows
    3. checking the values
    :param user_query: a string containing the user query
    :return:
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    #
    if len(result.columns) != len(solution_df.columns):
        st.write("The number of columns is wrong")
    elif result.shape[0] != solution_df.shape[0]:
        st.write("The number of rows is not the same")
    else:
        try:
            result = result[solution_df.columns]
            st.dataframe(result.compare(solution_df))
        except KeyError as e:
            st.write("Some columns are missing")


con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

import streamlit as st

st.markdown(
    """
    <h1 style='text-align: center;'>SQL SRS</h1>
    <p style='text-align: center;'>Spaced Repetition System SQL Practice</p>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()

    theme = st.selectbox(
        "What would you like to review",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )

    if theme:
        st.write("You selected:", theme)
        exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}' ")\
            .df()\
            .sort_values("last_reviewed")\
            .reset_index(drop=True)
    else:
        exercise = con.execute(f"SELECT * FROM memory_state") \
            .df() \
            .sort_values("last_reviewed") \
            .reset_index()
    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]




    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
    solution_df = con.execute(answer).df()



st.header("Enter your code")
form = st.form("my_form")
query = form.text_area(label="Your SQL code here", key="user_input")
form.form_submit_button("Submit")



if query:
    check_user_solution(query)

col1, col2, col3, col4 = st.columns(4)
n_days_list = [2, 7, 21]

with col1:
    if st.button(f"See again in {n_days_list[0]} days"):
        next_review = date.today() + timedelta(days=n_days_list[0])
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()

with col2:
    if st.button(f"See again in {n_days_list[1]} days"):
        next_review = date.today() + timedelta(days=n_days_list[1])
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()

with col3:
    if st.button(f"See again in {n_days_list[2]} days"):
        next_review = date.today() + timedelta(days=n_days_list[2])
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()


with col4:
    if st.button("Reset"):
        con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
        st.rerun()
tab1, tab2 = st.tabs(["Tables", "Solution"])
#
with tab1:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        st.dataframe(con.execute(f"SELECT * FROM {table}"))


with tab2:
    st.write(answer)
