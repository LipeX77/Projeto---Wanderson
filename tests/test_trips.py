from borajunto.models.trip import Trip
from borajunto.models.member import TripMember
from tests.conftest import login

def test_list_trips_requires_login(client):
    response = client.get("/trips/")
    assert response.status_code == 302

def test_create_trip(client, create_user, app):
    user = create_user(email="t1@t.com")
    login(client, "t1@t.com", "password123")
    response = client.post("/trips/new", data={
        "title": "Summer Trip",
        "destination": "Beach",
        "start_date": "2026-01-01",
        "end_date": "2026-01-10",
        "description": ""
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Summer Trip" in response.data
    
    with app.app_context():
        trip = Trip.query.filter_by(title="Summer Trip").first()
        assert trip is not None
        assert trip.owner_id == user.id
        member = TripMember.query.filter_by(trip_id=trip.id, user_id=user.id).first()
        assert member.role == "owner"

def test_list_trips(client, create_user, create_trip):
    user = create_user(email="l@t.com")
    create_trip(owner=user, title="My List Trip")
    login(client, "l@t.com", "password123")
    response = client.get("/trips/")
    assert b"My List Trip" in response.data

def test_detail_trip_member(client, create_user, create_trip):
    user = create_user(email="d@t.com")
    trip = create_trip(owner=user, title="Detail Trip")
    login(client, "d@t.com", "password123")
    response = client.get(f"/trips/{trip.id}")
    assert response.status_code == 200
    assert b"Detail Trip" in response.data

def test_detail_trip_not_member_403(client, create_user, create_trip):
    owner = create_user(email="o@t.com")
    trip = create_trip(owner=owner)
    intruder = create_user(email="i@t.com")
    login(client, "i@t.com", "password123")
    response = client.get(f"/trips/{trip.id}")
    assert response.status_code == 403
