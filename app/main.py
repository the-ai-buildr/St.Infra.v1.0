import streamlit as st

from app.auth import get_authenticator, require_login

st.set_page_config(
    page_title="Streamlit App",
    page_icon=":material/dashboard:",
    layout="wide",
)

name, username = require_login()

auth = get_authenticator()
auth.logout(location="sidebar")
st.sidebar.write(f"Logged in as **{name}**")


def _home() -> None:
    st.title("Welcome")
    st.write(f"Hello, {name}! Add your pages in `app/pages/` and register them below.")


home_page = st.Page(_home, title="Home", icon=":material/home:")
pg = st.navigation([home_page])
pg.run()
