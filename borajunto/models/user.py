from datetime import datetime, UTC
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from borajunto.ext.db import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)

    owned_trips = db.relationship("Trip", back_populates="owner", cascade="all, delete-orphan")
    trip_memberships = db.relationship("TripMember", back_populates="user", cascade="all, delete-orphan")
    created_invites = db.relationship("TripInvite", back_populates="created_by", cascade="all, delete-orphan")
    assigned_tasks = db.relationship("Task", foreign_keys="Task.assignee_id", back_populates="assignee", cascade="all, delete-orphan")
    created_tasks = db.relationship("Task", foreign_keys="Task.created_by_id", back_populates="created_by", cascade="all, delete-orphan")
    uploaded_attachments = db.relationship("Attachment", back_populates="uploaded_by", cascade="all, delete-orphan")
    uploaded_photos = db.relationship("Photo", back_populates="uploaded_by", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"
