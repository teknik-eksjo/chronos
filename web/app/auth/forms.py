from wtforms import (BooleanField,
                     PasswordField,
                     StringField,
                     SubmitField)

from wtforms.validators import (Email,
                                EqualTo,
                                Length,
                                Regexp,
                                Required)

from ..models import User
from flask_wtf import Form
from wtforms import ValidationError


class LoginForm(Form):
    email = StringField('Email', validators=[Required(),
                                             Length(1, 64),
                                             Email()])
    password = PasswordField('Lösenord', validators=[Required()])
    remember_me = BooleanField('Håll mig inloggad')
    submit = SubmitField('Logga in')


class ChangePasswordForm(Form):
    old_password = PasswordField('Gammalt lösenord', validators=[Required()])
    password = PasswordField('Nytt lösenord', validators=[Required(),
                                                          EqualTo('password2',
                                                          message='Lösenorden måste matcha')])
    password2 = PasswordField('Verfiera nytt lösenord', validators=[Required()])
    submit = SubmitField('Byt lösenord')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(),
                                             Length(1, 64),
                                             Email()])
    submit = SubmitField('Återställ lösenord')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(),
                                             Length(1, 64),
                                             Email()])
    password = PasswordField('Nytt lösenord', validators=[Required(),
                                                          EqualTo('password2',
                                                          message='Lösenorden måste matcha')])
    password2 = PasswordField('Verfiera lösenord', validators=[Required()])
    submit = SubmitField('Återställ lösenord')

    def validate_email(self, field):
        """Used to check if the email adress already exists in the database."""
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Okänd email-adress.')


class ChangeEmailForm(Form):
    email = StringField('Ny Email', validators=[Required(),
                                                Length(1, 64),
                                                Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Uppdatera Email-adress')

    def validate_email(self, field):
        """Used to check if the email adress already exists in the database.

        Raises an ValidationError if the email-adress is already registrated.
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email-adressen är redan registrerad.')
