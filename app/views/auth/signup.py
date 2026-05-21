import streamlit as st


def render() -> None:
    st.title("Sign Up")
    st.info("Signup flow to be implemented.")

    if st.button("Back to Login"):
        st.switch_page("app/views/auth/login.py")


render()
