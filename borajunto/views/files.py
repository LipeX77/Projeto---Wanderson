import os
from flask import Blueprint, abort, send_file
from flask_login import login_required, current_user
from borajunto.ext.db import db
from borajunto.models.attachment import Attachment
from borajunto.services.permissions import is_trip_member

bp_files = Blueprint("files", __name__, url_prefix="/files")

@bp_files.route("/<int:attachment_id>/download")
@login_required
def download_attachment(attachment_id):
    attachment = db.get_or_404(Attachment, attachment_id)
    
    if not is_trip_member(attachment.trip_id, current_user.id):
        abort(403)
        
    if not os.path.exists(attachment.storage_path):
        abort(404)
        
    return send_file(
        attachment.storage_path,
        as_attachment=True,
        download_name=attachment.original_name,
        mimetype=attachment.mime_type
    )

@bp_files.route("/<int:attachment_id>/preview")
@login_required
def preview_attachment(attachment_id):
    attachment = db.get_or_404(Attachment, attachment_id)
    
    if not is_trip_member(attachment.trip_id, current_user.id):
        abort(403)
        
    if not os.path.exists(attachment.storage_path):
        abort(404)
        
    is_image_ext = attachment.original_name.split(".")[-1].lower() in {"jpg", "jpeg", "png", "webp", "gif"}
    is_image_mime = attachment.mime_type and attachment.mime_type.startswith("image/")
    
    if not (is_image_ext or is_image_mime):
        abort(400)
        
    return send_file(
        attachment.storage_path,
        as_attachment=False,
        mimetype=attachment.mime_type
    )
