from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class TripForm(FlaskForm):
    title = StringField("Título da Viagem", validators=[DataRequired(), Length(min=3, max=120)])
    destination = StringField("Destino", validators=[DataRequired(), Length(min=2, max=120)])
    start_date = DateField("Data de Início", format="%Y-%m-%d", validators=[DataRequired()])
    end_date = DateField("Data de Término", format="%Y-%m-%d", validators=[DataRequired()])
    description = TextAreaField("Descrição (Opcional)", validators=[Length(max=1000)])
    submit = SubmitField("Salvar Viagem")

    def validate_end_date(self, field):
        if self.start_date.data and field.data:
            if field.data < self.start_date.data:
                raise ValidationError("A data de término não pode ser anterior à data de início.")
