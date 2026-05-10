import io
from borajunto.models.photo import Photo
from borajunto.models.attachment import Attachment
from tests.conftest import login

def test_upload_photo(client, create_user, create_trip, app):
    user = create_user(email="u@gal.com")
    trip = create_trip(owner=user)
    login(client, "u@gal.com", "password123")
    
    data = {
        "file": (io.BytesIO(b"fake image content"), "photo.png"),
        "caption": "My Vacation"
    }
    response = client.post(f"/trips/{trip.id}/gallery/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
    
    with app.app_context():
        photo = Photo.query.filter_by(trip_id=trip.id).first()
        assert photo is not None
        assert photo.caption == "My Vacation"
        assert photo.attachment.file_type == "photo"

def test_list_photos(client, create_user, create_trip, app):
    user = create_user(email="u2@gal.com")
    trip = create_trip(owner=user)
    login(client, "u2@gal.com", "password123")
    
    with app.app_context():
        from borajunto.ext.db import db
        att = Attachment(trip_id=trip.id, uploaded_by_id=user.id, original_name="p.png", stored_name="p.png", storage_path="/dev/null")
        db.session.add(att)
        photo = Photo(trip_id=trip.id, attachment=att, uploaded_by_id=user.id, caption="Show me")
        db.session.add(photo)
        db.session.commit()
        
    response = client.get(f"/trips/{trip.id}/gallery/")
    assert b"Show me" in response.data

def test_preview_photo(client, create_user, create_trip, app):
    user = create_user(email="u3@gal.com")
    trip = create_trip(owner=user)
    login(client, "u3@gal.com", "password123")
    
    with app.app_context():
        from borajunto.ext.db import db
        import os
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], "photo.png"))
        with open(path, "wb") as f:
            f.write(b"image_data")
            
        att = Attachment(trip_id=trip.id, uploaded_by_id=user.id, original_name="photo.png", stored_name="photo.png", storage_path=path, mime_type="image/png")
        db.session.add(att)
        db.session.commit()
        att_id = att.id
        
    response = client.get(f"/files/{att_id}/preview")
    assert response.status_code == 200
    assert response.data == b"image_data"
    
def test_delete_photo(client, create_user, create_trip, app):
    user = create_user(email="u4@gal.com")
    trip = create_trip(owner=user)
    login(client, "u4@gal.com", "password123")
    
    with app.app_context():
        from borajunto.ext.db import db
        import os
        path = os.path.abspath("del.png")
        att = Attachment(trip_id=trip.id, uploaded_by_id=user.id, original_name="del.png", stored_name="del.png", storage_path=path)
        db.session.add(att)
        photo = Photo(trip_id=trip.id, attachment=att, uploaded_by_id=user.id)
        db.session.add(photo)
        db.session.commit()
        p_id = photo.id
        
    response = client.post(f"/trips/{trip.id}/gallery/{p_id}/delete", follow_redirects=True)
    with app.app_context():
        from borajunto.ext.db import db
        p = db.session.get(Photo, p_id)
        assert p is None

def test_preview_photo_not_member(client, create_user, create_trip, app):
    owner = create_user(email="o@gal.com")
    trip = create_trip(owner=owner)
    intruder = create_user(email="i@gal.com")
    login(client, "i@gal.com", "password123")
    
    with app.app_context():
        from borajunto.ext.db import db
        import os
        path = os.path.abspath("photo.png")
        att = Attachment(trip_id=trip.id, uploaded_by_id=owner.id, original_name="photo.png", stored_name="photo.png", storage_path=path, mime_type="image/png")
        db.session.add(att)
        db.session.commit()
        att_id = att.id
        
    response = client.get(f"/files/{att_id}/preview")
    assert response.status_code == 403
