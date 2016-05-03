from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from wtforms.fields.html5 import DateField
from ..models import User
import re


class AddTeacherForm(Form):
    first_name = StringField('Förnamn', validators=[
        Required(), Length(1, 64), Regexp('^[A-Ö]*(-| )?[A-Ö]*(-| )?[A-Ö]*$', re.IGNORECASE,
                                          'Förnamn får endast innehålla A-Ö, a-ö, mellanslag och -.')])
    last_name = StringField('Efternamn', validators=[
        Required(), Length(1, 64), Regexp('^[A-Ö]*(-| )?[A-Ö]*(-| )?[A-Ö]*$', re.IGNORECASE,
                                          'Efternamn får endast innehålla A-Ö, a-ö, mellanslag och -.')])
    email = StringField('E-post', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Lägg till')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Epost är redan registrerad.')


class EditTeacherForm(Form):
    first_name = StringField('Förnamn', validators=[
        Required(), Length(1, 64), Regexp('^[A-Ö]*(-| )?[A-Ö]*(-| )?[A-Ö]*$', re.IGNORECASE,
                                          'Förnamn får endast innehålla A-Ö, a-ö, mellanslag och -.')])
    last_name = StringField('Efternamn', validators=[
        Required(), Length(1, 64), Regexp('^[A-Ö]*(-| )?[A-Ö]*(-| )?[A-Ö]*$', re.IGNORECASE,
                                          'Efternamn får endast innehålla A-Ö, a-ö, mellanslag och -.')])
    email = StringField('E-post', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Spara')


class ExcelUploadForm(Form):
    upload = FileField('Excel-dokument', validators=[FileRequired(), FileAllowed(['xlsx'])])


class AddWorkPeriodForm(Form):
    start = DateField('Startdatum', format='%Y-%m-%d', validators=[Required()])
    end = DateField('Slutdatum', format='%Y-%m-%d', validators=[Required()])
    submit = SubmitField('Spara')


class EditWorkPeriodForm(Form):
    start = DateField('Startdatum', format='%Y-%m-%d', validators=[Required()])
    end = DateField('Slutdatum', format='%Y-%m-%d', validators=[Required()])
    submit = SubmitField('Spara')
