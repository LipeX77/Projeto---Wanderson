import click
from flask.cli import with_appcontext

def init_app(app):
    @app.cli.command("init-db")
    @with_appcontext
    def init_db():
        """Inicializa o banco de dados criando as tabelas."""
        from borajunto.ext.db import db
        from borajunto import models  # noqa: F401

        db.create_all()
        click.echo("Banco de dados inicializado com sucesso.")
