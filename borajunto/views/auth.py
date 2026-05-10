from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from borajunto.forms.auth import RegisterForm, LoginForm
from borajunto.models.user import User
from borajunto.ext.db import db

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")

@bp_auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("Este e-mail já está em uso.", "danger")
            return redirect(url_for("auth.register"))
        
        new_user = User(name=form.name.data, email=form.email.data)
        new_user.set_password(form.password.data)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Conta criada com sucesso! Faça o login.", "success")
        return redirect(url_for("auth.login"))
        
    return render_template("auth/register.html", form=form)

@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login realizado com sucesso!", "success")
            
            # Simple redirect for this step, no complex next parsing needed
            return redirect(url_for("auth.profile"))
        else:
            flash("E-mail ou senha incorretos.", "danger")
            
    return render_template("auth/login.html", form=form)

@bp_auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("main.index"))

@bp_auth.route("/profile")
@login_required
def profile():
    return render_template("auth/profile.html")
