from datetime import datetime, UTC
from borajunto.ext.db import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False, index=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending", nullable=False)
    priority = db.Column(db.String(20), default="medium", nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    trip = db.relationship("Trip", back_populates="tasks")
    assignee = db.relationship("User", foreign_keys=[assignee_id], back_populates="assigned_tasks")
    created_by = db.relationship("User", foreign_keys=[created_by_id], back_populates="created_tasks")
    attachments = db.relationship("Attachment", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task {self.title}>"
