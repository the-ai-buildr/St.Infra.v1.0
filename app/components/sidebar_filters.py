import streamlit as st


def render_filters() -> None:
    st.sidebar.header("Filters")
    st.sidebar.selectbox("Project", ["All Projects", "Project A", "Project B"])
    st.sidebar.date_input("Date Range", [])
