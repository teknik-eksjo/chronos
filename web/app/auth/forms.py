from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Lösenord', validators=[Required()])
    remember_me = BooleanField('Håll mig inloggad')
    submit = SubmitField('Logga in')


class ChangePasswordForm(Form):
    old_password = PasswordField('Gammalt lösenord', validators=[Required()])
    password = PasswordField('Nytt lösenord', validators=[
        Required(), EqualTo('password2', message='Lösenorden måste matcha')])
    password2 = PasswordField('Verfiera nytt lösenord', validators=[Required()])
    submit = SubmitField('Byt lösenord')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Återställ lösenord')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Nytt lösenord', validators=[
        Required(), EqualTo('password2', message='Lösenorden måste matcha')])
    password2 = PasswordField('Verfiera lösenord', validators=[Required()])
    submit = SubmitField('Återställ lösenord')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Okänd email-adress.')


class ChangeEmailForm(Form):
    email = StringField('Ny Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Uppdatera Email-adress')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email-adressen är redan registrerad.')