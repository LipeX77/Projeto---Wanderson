from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import Length, Optional

class PhotoForm(FlaskForm):
    file = FileField("Arquivo da Imagem", validators=[FileRequired()])
    caption = StringField("Legenda (Opcional)", validators=[Optional(), Length(max=255)])
    taken_at = DateField("Data da Foto", format="%Y-%m-%d", validators=[Optional()])
    submit = SubmitField("Enviar foto")
