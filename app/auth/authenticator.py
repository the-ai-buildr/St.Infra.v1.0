import streamlit as st
import streamlit_authenticator as sa

from app.config.settings import settings
from app.db.session import SessionLocal
from app.models.user import User


def load_users_from_db() -> dict:
    """Loads users from the DB into the format streamlit-authenticator expects."""
    credentials = {"usernames": {}}
    try:
        with SessionLocal() as db:
            users = db.query(User).filter(User.is_active).all()
            for user in users:
                # Use email as the username key
                credentials["usernames"][user.email] = {
                    "name": user.name,
                    "email": user.email,
                    "password": user.hashed_password,
                }
    except Exception as e:
        print(f"Error loading users from DB: {e}")
        # Fallback to dev credentials if DB fails to load or tables aren't created yet
        credentials = {
            "usernames": {
                "test@local.dev": {
                    "name": "Test User",
                    "email": "test@local.dev",
                    "password": "dev1234",  # auto_hash=True bcrypts this
                }
            }
        }

    if not credentials["usernames"]:
        # Ensure we have at least one valid key even if DB is empty
        credentials = {
            "usernames": {
                "test@local.dev": {
                    "name": "Test User",
                    "email": "test@local.dev",
                    "password": "dev1234",
                }
            }
        }
    return credentials


def get_authenticator() -> sa.Authenticate:
    if "authenticator" not in st.session_state:
        credentials = load_users_from_db()
        st.session_state["authenticator"] = sa.Authenticate(
            credentials=credentials,
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
