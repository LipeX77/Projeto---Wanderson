import os
import tempfile
import pytest
from borajunto import create_app
from borajunto.ext.db import db
from borajunto.models.user import User
from borajunto.models.trip import Trip
from borajunto.models.member import TripMember
from borajunto.models.task import Task
from datetime import date

@pytest.fixture
def app():
    app = create_app("testing")
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def register(client, name, email, password):
    return client.post(
        '/auth/register',
        data=dict(name=name, email=email, password=password, confirm_password=password),
        follow_redirects=True
    )

def login(client, email, password):
    return client.post(
        '/auth/login',
        data=dict(email=email, password=password),
        follow_redirects=True
    )

def logout(client):
    return client.get('/auth/logout', follow_redirects=True)

@pytest.fixture
def create_user(app):
    def _create_user(name="Test User", email="test@example.com", password="password123"):
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    return _create_user

@pytest.fixture
def create_trip(app):
    def _create_trip(owner, title="Trip", dest="Dest", start=date(2026,1,1), end=date(2026,1,10)):
        trip = Trip(title=title, destination=dest, start_date=start, end_date=end, owner_id=owner.id)
        db.session.add(trip)
        db.session.flush()
        member = TripMember(trip_id=trip.id, user_id=owner.id, role="owner")
        db.session.add(member)
        db.session.commit()
        return trip
    return _create_trip

@pytest.fixture
def create_task(app):
    def _create_task(trip, creator, title="Task", status="pending"):
        task = Task(trip_id=trip.id, created_by_id=creator.id, title=title, status=status)
        db.session.add(task)
        db.session.commit()
        return task
    return _create_task
