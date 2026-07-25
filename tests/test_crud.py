"""
Tests user creation and lookup (database/crud.py).
Requires the MySQL database to be reachable and tables created
(`python database/create_tables.py`).
Run with: pytest tests/test_crud.py
"""

import pytest

from database.database import SessionLocal
from database.crud import create_user, get_user_by_email


TEST_EMAIL = "test_crud_user@example.com"


@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def _get_or_create_test_user(db):
    user = get_user_by_email(db, TEST_EMAIL)

    if user is None:
        user = create_user(
            db,
            name="Test CRUD User",
            email=TEST_EMAIL,
            password="test12345"
        )

    return user


def test_create_user_returns_user(db_session):
    user = _get_or_create_test_user(db_session)

    assert user is not None
    assert user.email == TEST_EMAIL


def test_get_user_by_email_finds_created_user(db_session):
    _get_or_create_test_user(db_session)

    found = get_user_by_email(db_session, TEST_EMAIL)

    assert found is not None
    assert found.email == TEST_EMAIL
    assert found.name == "Test CRUD User"


def test_create_user_rejects_duplicate_email(db_session):
    _get_or_create_test_user(db_session)

    duplicate = create_user(
        db_session,
        name="Someone Else",
        email=TEST_EMAIL,
        password="different-password"
    )

    assert duplicate is None