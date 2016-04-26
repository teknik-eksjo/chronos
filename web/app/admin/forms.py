from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User


class AddTeacherForm(Form):
    first_name = StringField('Förnamn', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    last_name = StringField('Efternamn', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    email2 = StringField('Verfiera Email', validators=[Required(),
                                                       EqualTo('email',
                                                               message='Email måste vara samma i båda fälten.'),
                                                       Email()])
    submit = SubmitField('Lägg till')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Epost är redan registrerad.')


class ExcelUploadForm(Form):
    upload = FileField('Excel-dokument', validators=[FileRequired(), FileAllowed(['xlsx'])])
