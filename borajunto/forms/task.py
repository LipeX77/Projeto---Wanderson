from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class TaskForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(min=3, max=120)])
    description = TextAreaField("Descrição", validators=[Optional(), Length(max=1000)])
    assignee_id = SelectField("Responsável", coerce=int, validators=[Optional()])
    due_date = DateField("Data de Entrega", format="%Y-%m-%d", validators=[Optional()])
    priority = SelectField("Prioridade", choices=[("low", "Baixa"), ("medium", "Média"), ("high", "Alta")], validators=[DataRequired()])
    submit = SubmitField("Salvar tarefa")

class StatusForm(FlaskForm):
    status = SelectField("Status", choices=[("pending", "Pendente"), ("doing", "Em andamento"), ("done", "Concluída")], validators=[DataRequired()])
    submit = SubmitField("Atualizar status")
