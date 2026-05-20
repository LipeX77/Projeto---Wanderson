from flask import Blueprint, render_template, current_app

bp_main = Blueprint("main", __name__)


@bp_main.route("/")
@bp_main.route("/index")
def index():
    current_app.logger.info("Página inicial acessada")
    return render_template("main/index.html")