from borajunto.models.invite import TripInvite
from borajunto.models.member import TripMember
from tests.conftest import login

def test_invites_page_owner(client, create_user, create_trip):
    owner = create_user(email="o@i.com")
    trip = create_trip(owner)
    login(client, "o@i.com", "password123")
    response = client.get(f"/trips/{trip.id}/invite")
    assert response.status_code == 200

def test_generate_invite(client, create_user, create_trip, app):
    owner = create_user(email="o2@i.com")
    trip = create_trip(owner)
    login(client, "o2@i.com", "password123")
    response = client.post(f"/trips/{trip.id}/invite/generate", follow_redirects=True)
    with app.app_context():
        from borajunto.ext.db import db
        invite = TripInvite.query.filter_by(trip_id=trip.id).first()
        assert invite is not None
        assert invite.token.encode('utf-8') in response.data

def test_join_trip_success(client, create_user, create_trip, app):
    owner = create_user(email="o3@i.com")
    trip = create_trip(owner)
    with app.app_context():
        from borajunto.ext.db import db
        invite = TripInvite(trip_id=trip.id, created_by_id=owner.id, token="abc123token")
        db.session.add(invite)
        db.session.commit()
    
    user_b = create_user(email="b@i.com")
    login(client, "b@i.com", "password123")
    response = client.get("/trips/join/abc123token", follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        member = TripMember.query.filter_by(trip_id=trip.id, user_id=user_b.id).first()
        assert member is not None
        assert member.role == "member"

def test_join_trip_already_member(client, create_user, create_trip, app):
    owner = create_user(email="o4@i.com")
    trip = create_trip(owner)
    with app.app_context():
        from borajunto.ext.db import db
        invite = TripInvite(trip_id=trip.id, created_by_id=owner.id, token="already")
        db.session.add(invite)
        db.session.commit()
    
    login(client, "o4@i.com", "password123")
    response = client.get("/trips/join/already", follow_redirects=True)
    assert response.status_code == 200

def test_join_trip_invalid_token(client, create_user):
    user = create_user()
    login(client, user.email, "password123")
    response = client.get("/trips/join/invalid", follow_redirects=True)
    assert response.status_code in [404, 200]
    if response.status_code == 200:
        assert b"expirado" in response.data or b"invalido" in response.data.lower() or b"inv\xc3\xa1lido" in response.data.lower()

def test_not_owner_generate_invite(client, create_user, create_trip, app):
    owner = create_user(email="o5@i.com")
    trip = create_trip(owner)
    intruder = create_user(email="i2@i.com")
    
    with app.app_context():
        from borajunto.ext.db import db
        m = TripMember(trip_id=trip.id, user_id=intruder.id, role="member")
        db.session.add(m)
        db.session.commit()
        
    login(client, "i2@i.com", "password123")
    response = client.post(f"/trips/{trip.id}/invite/generate")
    assert response.status_code == 403
