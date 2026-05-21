def test_settings_load():
    from app.config import settings

    assert settings.POSTGRES_DB == "streamlit_app"
    assert settings.APP_ENV in ("local", "staging", "production")


def test_database_url_assembled():
    from app.config import settings

    assert "postgresql" in settings.DATABASE_URL
    assert settings.POSTGRES_HOST in settings.DATABASE_URL
    assert settings.POSTGRES_DB in settings.DATABASE_URL


def test_async_database_url_uses_asyncpg():
    from app.config import settings

    assert "asyncpg" in settings.ASYNC_DATABASE_URL
