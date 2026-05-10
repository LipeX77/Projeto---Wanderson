from datetime import datetime, UTC
from borajunto.ext.db import db

class TripInvite(db.Model):
    __tablename__ = "trip_invites"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False, index=True)
    token = db.Column(db.String(64), unique=True, index=True, nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    uses = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)

    trip = db.relationship("Trip", back_populates="invites")
    created_by = db.relationship("User", back_populates="created_invites")

    def __repr__(self):
        return f"<TripInvite {self.token}>"
