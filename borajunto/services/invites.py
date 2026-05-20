import secrets
from datetime import datetime, UTC
from borajunto.ext.db import db
from borajunto.models.invite import TripInvite

def generate_invite_token():
    return secrets.token_urlsafe(24)

def create_trip_invite(trip, created_by):
    invite = TripInvite(
        trip_id=trip.id,
        token=generate_invite_token(),
        created_by_id=created_by.id
    )
    db.session.add(invite)
    db.session.commit()
    return invite

def get_valid_invite_by_token(token):
    invite = TripInvite.query.filter_by(token=token).first()
    if not invite or not invite.is_active:
        return None
    
    if invite.expires_at and invite.expires_at < datetime.now(UTC):
        return None
        
    return invite
