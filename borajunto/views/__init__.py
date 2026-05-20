from borajunto.views.main import bp_main
from borajunto.views.auth import bp_auth
from borajunto.views.trips import bp_trips
from borajunto.views.tasks import bp_tasks
from borajunto.views.files import bp_files
from borajunto.views.gallery import bp_gallery

def init_app(app):
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_trips)
    app.register_blueprint(bp_tasks)
    app.register_blueprint(bp_files)
    app.register_blueprint(bp_gallery)
