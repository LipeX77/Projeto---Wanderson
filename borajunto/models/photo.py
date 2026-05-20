from datetime import datetime, UTC
from borajunto.ext.db import db

class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False, index=True)
    attachment_id = db.Column(db.Integer, db.ForeignKey("attachments.id"), nullable=False, unique=True, index=True)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    caption = db.Column(db.String(255), nullable=True)
    taken_at = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)

    trip = db.relationship("Trip", back_populates="photos")
    attachment = db.relationship("Attachment", back_populates="photo")
    uploaded_by = db.relationship("User", back_populates="uploaded_photos")

    def __repr__(self):
        return f"<Photo {self.id}>"
