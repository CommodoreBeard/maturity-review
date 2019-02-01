from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from flask_wtf.file import FileField, FileRequired

class CsvForm(FlaskForm):
    csv = FileField(validators=[FileRequired()])
    submit = SubmitField(u'Upload')