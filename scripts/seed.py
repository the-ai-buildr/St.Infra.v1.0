"""
Seed development data.
Run via: make seed

Extend this script as your schema grows.
"""

from app.config.settings import settings
from app.db.session import get_db


def main() -> None:
    print(f"Seeding {settings.APP_ENV} database: {settings.POSTGRES_DB}")
    with get_db() as db:  # noqa: F841
        # Add seed logic here once models exist. Example:
        # from app.models.user import User
        # if not db.query(User).filter_by(email="test@local.dev").first():
        #     db.add(User(email="test@local.dev", hashed_password=...))
        pass
    print("Seed complete.")
    print("  Auth credentials (hardcoded in app/auth.py):")
    print("    Email:    test@local.dev")
    print("    Password: dev1234")


if __name__ == "__main__":
    main()
