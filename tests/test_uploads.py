import io
from borajunto.models.attachment import Attachment
from tests.conftest import login

def test_upload_task_attachment(client, create_user, create_trip, create_task, app):
    user = create_user(email="u@upl.com")
    trip = create_trip(owner=user)
    task = create_task(trip, user)
    login(client, "u@upl.com", "password123")
    
    data = {
        "file": (io.BytesIO(b"dummy pdf content"), "test.pdf")
    }
    response = client.post(f"/trips/{trip.id}/tasks/{task.id}/attachments/new", data=data, content_type="multipart/form-data", follow_redirects=True)
    
    with app.app_context():
        att = Attachment.query.filter_by(trip_id=trip.id).first()
        assert att is not None
        assert att.original_name == "test.pdf"
        assert att.file_type == "task_proof"

def test_download_attachment_member(client, create_user, create_trip, app):
    user = create_user(email="u2@upl.com")
    trip = create_trip(owner=user)
    login(client, "u2@upl.com", "password123")
    
    with app.app_context():
        from borajunto.ext.db import db
        import os
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], "test.pdf"))
        with open(path, "wb") as f:
            f.write(b"content")
        att = Attachment(trip_id=trip.id, uploaded_by_id=user.id, original_name="test.pdf", stored_name="test.pdf", storage_path=path)
        db.session.add(att)
        db.session.commit()
        att_id = att.id
        
    response = client.get(f"/files/{att_id}/download")
    assert response.status_code == 200
    assert response.data == b"content"

def test_download_attachment_not_member(client, create_user, create_trip, app):
    owner = create_user(email="o@upl.com")
    trip = create_trip(owner)
    intruder = create_user(email="i@upl.com")
    login(client, "i@upl.com", "password123")
    
    with app.app_context():
        from borajunto.ext.db import db
        import os
        path = os.path.abspath("dummy.pdf")
        att = Attachment(trip_id=trip.id, uploaded_by_id=owner.id, original_name="test.pdf", stored_name="test.pdf", storage_path=path)
        db.session.add(att)
        db.session.commit()
        att_id = att.id
        
    response = client.get(f"/files/{att_id}/download")
    assert response.status_code == 403

def test_upload_invalid_extension(client, create_user, create_trip, create_task, app):
    user = create_user(email="u3@upl.com")
    trip = create_trip(owner=user)
    task = create_task(trip, user)
    login(client, "u3@upl.com", "password123")
    
    data = {
        "file": (io.BytesIO(b"virus"), "test.exe")
    }
    response = client.post(f"/trips/{trip.id}/tasks/{task.id}/attachments/new", data=data, content_type="multipart/form-data")
    assert b"permitido" in response.data or b"permitida" in response.data
