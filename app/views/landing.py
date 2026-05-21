import streamlit as st

from app.components.layout import hide_sidebar_css


def render() -> None:
    hide_sidebar_css()

    st.title("Welcome to the App")
    st.markdown("This is a reusable Streamlit data-app template.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Get Started", use_container_width=True, type="primary"):
            st.switch_page("app/views/auth/login.py")

        col_a, col_b = st.columns(2)
        with col_a:
            st.page_link("app/views/auth/signup.py", label="Sign up")
        with col_b:
            st.page_link("app/views/auth/forgot.py", label="Forgot password")


render()
