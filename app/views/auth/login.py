import streamlit as st

from app.auth.authenticator import get_authenticator


def render() -> None:
    st.title("Login")

    auth = get_authenticator()
    name, auth_status, username = auth.login(location="main")

    if auth_status is False:
        st.error("Incorrect username or password.")
    elif auth_status is None:
        st.info("Please log in to continue.")
    else:
        st.success(f"Welcome back, {name}!")
        if st.button("Go to Dashboard"):
            st.switch_page("app/views/dashboard.py")


render()
