from datetime import datetime, UTC
from borajunto.ext.db import db

class Attachment(db.Model):
    __tablename__ = "attachments"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False, index=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=True, index=True)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False)
    storage_path = db.Column(db.String(500), nullable=False)
    mime_type = db.Column(db.String(120), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)
    file_type = db.Column(db.String(30), default="document", nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)

    trip = db.relationship("Trip", back_populates="attachments")
    task = db.relationship("Task", back_populates="attachments")
    uploaded_by = db.relationship("User", back_populates="uploaded_attachments")
    photo = db.relationship("Photo", back_populates="attachment", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Attachment {self.original_name}>"
