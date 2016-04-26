from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User
import re


class AddTeacherForm(Form):
    first_name = StringField('Förnamn', validators=[
        Required(), Length(1, 64), Regexp('^[A-Ö]*(-| )?[A-Ö]*(-| )?[A-Ö]*$', re.IGNORECASE,
                                          'Förnamn får endast innehålla A-Ö, a-ö, mellanslag och -.')])
    last_name = StringField('Efternamn', validators=[
        Required(), Length(1, 64), Regexp('^[A-Ö]*(-| )?[A-Ö]*(-| )?[A-Ö]*$', re.IGNORECASE,
                                          'Efternamn får endast innehålla A-Ö, a-ö, mellanslag och -.')])
    email = StringField('Epost', validators=[Required(), Length(1, 64), Email()])
    email2 = StringField('Verfiera Epost', validators=[Required(),
                                                       EqualTo('email',
                                                               message='Epost måste vara samma i båda fält.'),
                                                       Email()])
    submit = SubmitField('Lägg till')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Epost är redan registrerad.')


class ExcelUploadForm(Form):
    upload = FileField('Excel-dokument', validators=[FileRequired(), FileAllowed(['xlsx'])])
