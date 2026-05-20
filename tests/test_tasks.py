from borajunto.models.task import Task
from tests.conftest import login

def test_create_task(client, create_user, create_trip, app):
    user = create_user(email="t1@tsk.com")
    trip = create_trip(owner=user)
    login(client, "t1@tsk.com", "password123")
    response = client.post(f"/trips/{trip.id}/tasks/new", data={
        "title": "Buy Tickets",
        "priority": "high",
        "assignee_id": user.id
    }, follow_redirects=True)
    with app.app_context():
        task = Task.query.filter_by(trip_id=trip.id).first()
        assert task is not None
        assert task.title == "Buy Tickets"
        assert task.assignee_id == user.id

def test_update_status(client, create_user, create_trip, create_task, app):
    user = create_user(email="t2@tsk.com")
    trip = create_trip(owner=user)
    task = create_task(trip, user, status="pending")
    login(client, "t2@tsk.com", "password123")
    response = client.post(f"/trips/{trip.id}/tasks/{task.id}/status", data={"status": "done"}, follow_redirects=True)
    with app.app_context():
        from borajunto.ext.db import db
        t = db.session.get(Task, task.id)
        assert t.status == "done"
        assert t.completed_at is not None

def test_delete_task(client, create_user, create_trip, create_task, app):
    user = create_user(email="t3@tsk.com")
    trip = create_trip(owner=user)
    task = create_task(trip, user)
    login(client, "t3@tsk.com", "password123")
    response = client.post(f"/trips/{trip.id}/tasks/{task.id}/delete", follow_redirects=True)
    with app.app_context():
        from borajunto.ext.db import db
        t = db.session.get(Task, task.id)
        assert t is None

def test_delete_task_not_member_403(client, create_user, create_trip, create_task):
    owner = create_user(email="o@tsk.com")
    trip = create_trip(owner)
    task = create_task(trip, owner)
    
    intruder = create_user(email="i@tsk.com")
    login(client, "i@tsk.com", "password123")
    response = client.post(f"/trips/{trip.id}/tasks/{task.id}/delete")
    assert response.status_code == 403
