import os
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from borajunto.ext.db import db
from borajunto.models.trip import Trip
from borajunto.models.photo import Photo
from borajunto.models.attachment import Attachment
from borajunto.forms.photo import PhotoForm
from borajunto.services.permissions import is_trip_member, can_manage_trip
from borajunto.services.uploads import allowed_image, save_uploaded_file

bp_gallery = Blueprint("gallery", __name__, url_prefix="/trips/<int:trip_id>/gallery")

@bp_gallery.route("/")
@login_required
def list_photos(trip_id):
    trip = db.get_or_404(Trip, trip_id)
    if not is_trip_member(trip_id, current_user.id):
        abort(403)
        
    photos = Photo.query.filter_by(trip_id=trip.id).order_by(
        db.desc(Photo.taken_at), 
        db.desc(Photo.created_at)
    ).all()
    
    return render_template("gallery/list.html", trip=trip, photos=photos)

@bp_gallery.route("/upload", methods=["GET", "POST"])
@login_required
def upload_photo(trip_id):
    trip = db.get_or_404(Trip, trip_id)
    if not is_trip_member(trip_id, current_user.id):
        abort(403)
        
    form = PhotoForm()
    
    if form.validate_on_submit():
        file = form.file.data
        if not allowed_image(file.filename):
            flash("Formato de imagem não permitido.", "danger")
            return render_template("gallery/upload.html", trip=trip, form=form)
            
        file_data = save_uploaded_file(file, subfolder="photos")
        if file_data:
            attachment = Attachment(
                trip_id=trip.id,
                task_id=None,
                uploaded_by_id=current_user.id,
                original_name=file_data["original_name"],
                stored_name=file_data["stored_name"],
                storage_path=file_data["storage_path"],
                mime_type=file_data["mime_type"],
                file_size=file_data["file_size"],
                file_type="photo"
            )
            
            photo = Photo(
                trip_id=trip.id,
                attachment=attachment,
                uploaded_by_id=current_user.id,
                caption=form.caption.data,
                taken_at=form.taken_at.data
            )
            
            db.session.add(attachment)
            db.session.add(photo)
            db.session.commit()
            
            flash("Foto enviada com sucesso!", "success")
            return redirect(url_for("gallery.list_photos", trip_id=trip.id))
            
    return render_template("gallery/upload.html", trip=trip, form=form)

@bp_gallery.route("/<int:photo_id>/delete", methods=["POST"])
@login_required
def delete_photo(trip_id, photo_id):
    photo = db.get_or_404(Photo, photo_id)
    
    if photo.trip_id != trip_id:
        abort(404)
        
    if not is_trip_member(trip_id, current_user.id):
        abort(403)
        
    if not (can_manage_trip(trip_id, current_user.id) or photo.uploaded_by_id == current_user.id):
        abort(403)
        
    attachment = photo.attachment
    
    db.session.delete(photo)
    if attachment:
        db.session.delete(attachment)
        
        if os.path.exists(attachment.storage_path):
            try:
                os.remove(attachment.storage_path)
            except OSError:
                pass
                
    db.session.commit()
    flash("Foto excluída com sucesso!", "success")
    
    return redirect(url_for("gallery.list_photos", trip_id=trip_id))
