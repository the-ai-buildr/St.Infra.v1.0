import streamlit as st


def render() -> None:
    st.title("Forgot Password")
    st.info("Forgot password flow to be implemented.")

    if st.button("Back to Login"):
        st.switch_page("app/views/auth/login.py")


render()
