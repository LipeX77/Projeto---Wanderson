from flask_login import LoginManager

login_manager = LoginManager()

def init_app(app):
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para acessar esta página."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from borajunto.models.user import User
    from borajunto.ext.db import db
    try:
        return db.session.get(User, int(user_id))
    except (ValueError, TypeError):
        return None
