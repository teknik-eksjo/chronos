import pytest
from app.models import User


def test_password_setter():
    u = User(password='supersecret')
    assert u.password_hash is not None


def test_no_password_getter():
    u = User(password='supersecret')
    with pytest.raises(AttributeError):
        u.password


def test_password_verification():
    u = User(password='cat')
    assert u.verify_password('cat')
    assert u.verify_password('dog') is False


def test_password_salts_are_random():
    u = User(password='cat')
    u2 = User(password='cat')
    assert u.password_hash != u2.password_hash


def test_valid_email_change(session):
    u = User(email='test@example.com')
    session.add(u)
    session.commit()

    token = u.generate_email_change_token('new-email@example.com')
    assert u.change_email(token)


def test_duplicate_email_change(session):
    u = User(email='test@example.com')
    u2 = User(email='old-email@example.com')
    session.add(u)
    session.add(u2)
    session.commit()

    token = u2.generate_email_change_token('test@example.com')
    # It's not possible to change to another user's email
    assert u2.change_email(token) is False


def test_invalid_email_change_token(session):
    u1 = User(email='john@example.com', password='cat')
    u2 = User(email='susan@example.org', password='dog')
    session.add(u1)
    session.add(u2)
    session.commit()
    token = u1.generate_email_change_token('david@example.net')
    # It's not possible to use another user's token
    assert u2.change_email(token) is False
    assert u2.email == 'susan@example.org'
