import streamlit as st

from app.auth.authenticator import require_login
from app.components.footer import render_sidebar_footer
from app.components.layout import inject_app_css


def render() -> None:
    inject_app_css()
    require_login()
    render_sidebar_footer()

    st.title("Preferences")
    st.info("Preferences page stub.")


render()
