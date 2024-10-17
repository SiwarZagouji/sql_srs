import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# answer_str = """
# SELECT * FROM beverages
# CROSS JOIN food_items
# """
# solution_df = duckdb.sql(answer_str).df()

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
    exercice = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}' ").df()
    st.write(exercice)


st.header("Enter your code")
query = st.text_input(label="your SQL code here", key="user_input")
# if query:
#     result = duckdb.query(query)
#     st.dataframe(result)
#
#     if len(result.columns) != len(solution_df.columns):
#         st.write("The number of columns is wrong")
#     if result.shape[0] != solution_df.shape[0]:
#         st.write("The number of rows is not the same")
#     try:
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#     except KeyError as e:
#         st.write("Some columns are missing")
#
#
# tab1, tab2 = st.tabs(["Tables", "Solution"])
#
# with tab1:
#     st.write("Table beverages")
#     st.dataframe(beverages)
#     st.write("Table food_items")
#     st.dataframe(food_items)
#     st.write("Expected")
#     st.dataframe(solution_df)
#
# with tab2:
#     st.write(answer_str)
