from datetime import datetime, UTC
from borajunto.ext.db import db

class TripMember(db.Model):
    __tablename__ = "trip_members"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    role = db.Column(db.String(20), default="member", nullable=False)
    joined_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)

    trip = db.relationship("Trip", back_populates="members")
    user = db.relationship("User", back_populates="trip_memberships")

    __table_args__ = (
        db.UniqueConstraint('trip_id', 'user_id', name='uq_trip_member'),
    )

    def __repr__(self):
        return f"<TripMember {self.trip_id} {self.user_id} {self.role}>"
