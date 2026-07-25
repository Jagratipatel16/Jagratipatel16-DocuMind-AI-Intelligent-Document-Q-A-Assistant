"""
Tests password hashing and verification (database/auth.py).
Run with: pytest tests/test_auth.py
"""

from database.auth import hash_password, verify_password


def test_hash_password_produces_different_string():
    password = "123456"
    hashed = hash_password(password)

    assert hashed != password
    assert isinstance(hashed, str)
    assert len(hashed) > 0


def test_verify_password_correct():
    password = "123456"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    password = "123456"
    hashed = hash_password(password)

    assert verify_password("wrong-password", hashed) is False