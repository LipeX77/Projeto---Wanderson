from datetime import datetime, UTC
from borajunto.ext.db import db

class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)

    owner = db.relationship("User", back_populates="owned_trips")
    members = db.relationship("TripMember", back_populates="trip", cascade="all, delete-orphan")
    invites = db.relationship("TripInvite", back_populates="trip", cascade="all, delete-orphan")
    tasks = db.relationship("Task", back_populates="trip", cascade="all, delete-orphan")
    attachments = db.relationship("Attachment", back_populates="trip", cascade="all, delete-orphan")
    photos = db.relationship("Photo", back_populates="trip", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trip {self.title}>"
