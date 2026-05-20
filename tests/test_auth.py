from borajunto.models.user import User

def test_register_get(client):
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert b"Criar Conta" in response.data

def test_register_post(client, app):
    from tests.conftest import register
    response = register(client, "New User", "new@test.com", "pass123")
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email="new@test.com").first()
        assert user is not None
        assert user.name == "New User"

def test_register_duplicate_email(client, create_user, app):
    create_user(email="dup@test.com")
    from tests.conftest import register
    response = register(client, "Another", "dup@test.com", "pass")
    assert response.status_code == 200
    with app.app_context():
        from borajunto.models.user import User
        assert User.query.filter_by(email="dup@test.com").count() == 1

def test_login_success(client, create_user):
    create_user(email="login@test.com", password="pwd")
    from tests.conftest import login
    response = login(client, "login@test.com", "pwd")
    assert b"Meu Perfil" in response.data

def test_login_wrong_password(client, create_user):
    create_user(email="log2@test.com", password="pwd")
    from tests.conftest import login
    response = login(client, "log2@test.com", "wrong")
    assert b"E-mail ou senha incorretos" in response.data

def test_logout(client, create_user):
    create_user(email="out@test.com", password="pwd")
    from tests.conftest import login, logout
    login(client, "out@test.com", "pwd")
    response = logout(client)
    assert b"BoraJunto" in response.data

def test_profile_requires_login(client):
    response = client.get("/auth/profile")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]

def test_profile_logged_in(client, create_user):
    create_user(email="prof@test.com", password="pwd")
    from tests.conftest import login
    login(client, "prof@test.com", "pwd")
    response = client.get("/auth/profile")
    assert response.status_code == 200
    assert b"Meu Perfil" in response.data
