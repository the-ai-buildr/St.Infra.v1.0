import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

landing_page = st.Page("app/views/landing.py", title="Home", icon=":material/home:")
login_page = st.Page("app/views/auth/login.py", title="Login", icon=":material/login:")
signup_page = st.Page(
    "app/views/auth/signup.py", title="Sign Up", icon=":material/person_add:"
)
forgot_page = st.Page(
    "app/views/auth/forgot.py", title="Forgot Password", icon=":material/password:"
)

dashboard_page = st.Page(
    "app/views/dashboard.py", title="Dashboard", icon=":material/dashboard:"
)
settings_page = st.Page(
    "app/views/settings.py", title="Settings", icon=":material/settings:"
)
preferences_page = st.Page(
    "app/views/preferences.py", title="Preferences", icon=":material/palette:"
)

if (
    "authentication_status" not in st.session_state
    or not st.session_state["authentication_status"]
):
    pg = st.navigation([landing_page, login_page, signup_page, forgot_page])
else:
    pg = st.navigation(
        {
            "App": [dashboard_page, settings_page, preferences_page],
        }
    )

pg.run()
