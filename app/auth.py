import streamlit as st
import streamlit_authenticator as sa

from app.config import settings

# Dev credentials — replace with DB-backed loader for production
_DEV_CREDENTIALS: dict = {
    "usernames": {
        "testuser": {
            "name": "Test User",
            "email": "test@local.dev",
            "password": "dev1234",  # auto_hash=True bcrypts this on first run
        }
    }
}


def get_authenticator() -> sa.Authenticate:
    if "authenticator" not in st.session_state:
        st.session_state["authenticator"] = sa.Authenticate(
            credentials=_DEV_CREDENTIALS,
            cookie_name="streamlit_app_auth",
            cookie_key=settings.AUTH_COOKIE_KEY.get_secret_value(),
            cookie_expiry_days=30,
            auto_hash=True,
        )
    return st.session_state["authenticator"]


def require_login() -> tuple[str, str]:
    """Call at the top of any protected page. Returns (name, username) or stops."""
    auth = get_authenticator()
    name, auth_status, username = auth.login(location="main")
    if auth_status is False:
        st.error("Incorrect username or password.")
        st.stop()
    if auth_status is None:
        st.info("Please log in to continue.")
        st.stop()
    return name, username
