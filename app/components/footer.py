import streamlit as st

from app.auth.authenticator import get_authenticator


def render_sidebar_footer() -> None:
    st.sidebar.markdown("---")

    st.sidebar.page_link("app/views/settings.py", label="Settings", icon="⚙️")
    st.sidebar.page_link("app/views/preferences.py", label="Preferences", icon="🎨")

    st.sidebar.markdown("---")
    auth = get_authenticator()
    auth.logout(location="sidebar")
