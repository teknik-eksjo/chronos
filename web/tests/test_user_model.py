import pytest
from app.models import User, Permission, Role
import time


def test_password_setter():
    u = User(password='supersecret')
    assert u.password_hash is not None


def test_no_password_getter():
    u = User(password='supersecret')
    with pytest.raises(AttributeError):
        u.password


def test_verify_password():
    u = User(password='cat')
    assert u.password_hash is not None
    assert u.verify_password('cat')
    assert u.verify_password('dog') is False


def test_reset_password(session):
    """Test the process of resetting password.

    Test wheter the password actually becomes changed when reset_password()
    is called.The process requires that generate_reset_token is working
    properly.
    """
    u = User(password='supersecret')
    session.add(u)
    session.commit()

    token = u.generate_reset_token()
    assert u.reset_password(token, "xyz")  # You should be able to reset the password
    assert u.verify_password("xyz")  # Checks wheter the password was changed properly
    assert u.reset_password("fail", "xyz") is False


def test_change_email(session):
    """Test the process of changing email.

    Test wheter the email actually becomes changed when change_email()
    is called.The process requires that generate_email_change_token is working
    properly.
    """
    u = User(email='test@example.com')
    u2 = User(email='old-email@example.com')
    session.add(u)
    session.add(u2)
    session.commit()

    token = u.generate_email_change_token('new-email@example.com')
    assert u.change_email(token)  # Checks wether it was possible to change email
    assert u.email == 'new-email@example.com'  # Checks wether the new email is correct
    assert u.change_email("xyz") is False
    assert u2.change_email(token) is False  # It's not possible to change to another user's email!


def test_invalid_email_change_token(session):
    """Test wheter it is impossible to change another users email."""
    u1 = User(email='john@example.com', password='cat')
    u2 = User(email='susan@example.org', password='dog')
    session.add(u1)
    session.add(u2)
    session.commit()

    token = u1.generate_email_change_token('david@example.net')
    assert u2.change_email(token) is False  # It's not possible to use another user's token
    assert u2.email == 'susan@example.org'
"""
def test_generate_email_login_token(session):
    '''Tests the login tokens for emails.'''
    u = User(email='len@example.com', password='fas')

    assert u.verify_password('fas')
    new = u.generate_email_login_token()
    assert u.verify_password(new)
    assert u.verify_password('fas') is False
"""


def test_password_salts_are_random():
    u = User(password='cat')
    u2 = User(password='cat')
    u3 = User(password='cat')
    assert u.password_hash != u2.password_hash
    assert u2.password_hash != u3.password_hash


def test_roles(session):
    """Test that the role system works properly."""
    u = User(role=Role.query.filter_by(name='Teacher').first())
    u2 = User(role=Role.query.filter_by(name='Principal').first())
    u3 = User(role=Role.query.filter_by(name='Moderator').first())
    u4 = User(role=Role.query.filter_by(name='Administrator').first())
    session.add(u)
    session.add(u2)
    session.add(u3)
    session.add(u4)
    session.commit()

    assert u.can(Permission.WRITE_SCHEDULE)
    assert u.can(Permission.APPROVE_SCHEDULE) is False
    assert u.can(Permission.READ_SCHEDULE) is False
    assert u.can(Permission.UNLOCK_SCHEDULE) is False
    assert u.can(Permission.CREATE_USER) is False
    assert u2.can(Permission.READ_SCHEDULE)
    assert u2.can(Permission.APPROVE_SCHEDULE)
    assert u2.can(Permission.UNLOCK_SCHEDULE)
    assert u2.can(Permission.CREATE_USER) is False
    assert u2.can(Permission.WRITE_SCHEDULE) is False
    assert u3.can(Permission.READ_SCHEDULE)
    assert u3.can(Permission.UNLOCK_SCHEDULE)
    assert u3.can(Permission.CREATE_USER)
    assert u3.can(Permission.WRITE_SCHEDULE) is False
    assert u3.can(Permission.APPROVE_SCHEDULE) is False
    assert u.is_administrator() is False
    assert u2.is_administrator() is False
    assert u3.is_administrator() is False
    assert u4.is_administrator()


def test_auth_token(session):
    """Test of auth tokens and expiration.

    Tests the generated token by generate_auth_token()
    works properly togheter with verify_auth_token(), and that the expiration system works properly
    """
    u = User(email='choli@example.com', password='cat')
    u2 = User(email='lenno@example.com', password='xyz')
    session.add(u)
    session.add(u2)
    session.commit()
    token = u.generate_auth_token(1)

    assert u.verify_auth_token(token) == u
    assert u.verify_auth_token(token) != u2  # The token for "u" should be linked to "u2"
    time.sleep(2)  # The token should have expired after 2 seconds
    assert u.verify_auth_token(token) != u
