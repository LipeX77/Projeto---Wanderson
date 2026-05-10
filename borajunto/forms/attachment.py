from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

class AttachmentForm(FlaskForm):
    file = FileField("Arquivo", validators=[FileRequired()])
    submit = SubmitField("Enviar comprovante")
