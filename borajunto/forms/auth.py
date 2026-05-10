from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(min=3, max=100)])
    email = EmailField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar Senha", validators=[
        DataRequired(), EqualTo("password", message="As senhas devem ser iguais.")
    ])
    submit = SubmitField("Criar Conta")

class LoginForm(FlaskForm):
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember = BooleanField("Lembrar-me")
    submit = SubmitField("Entrar")
