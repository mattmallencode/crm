from tests.classes_for_tests import UserForTests, InviteForTests

def test_login_required(client):

    # When the user is not authenticated
    response = client.get("/contacts")

    # Then the user should be redirected to the login page
    assert response.status_code == 302
    assert response.location.endswith("/login?next=http%3A%2F%2Flocalhost%2Fcontacts")

    with client:
        # Given an authenticated user
        with client.session_transaction() as session:
            session["email"] = "test@test.com"

        # When the user accesses the protected endpoint
        response = client.get("/contacts")

        # Then the user should be able to access the endpoint
        # In this case they're redirected to create_team as they don't have a team_id.
        assert response.status_code == 302
        assert response.location == "/create_team"

def test_login(client):
    # When a GET request is made to the login page
    response = client.get("/login")

    # Then the response should be successful and the login form should be displayed
    assert response.status_code == 200
    assert b"Login" in response.data

    # When a POST request is made with valid login credentials
    email = "123@123.com"
    password = "123"
    with client:
        response = client.post("/login", data={"email": email, "password": password})
        # Then the response should redirect to the home page
        assert response.status_code == 302
        assert response.location == "/"
    email = "testtesttest@testtesttest.com"
    password = "123"
    # When a POST request is made with a user that doesn't exist.
    with client:
        response = client.post("/login", data={"email": email, "password": password})
        # Then the response should keep us on the login page.
        assert response.status_code == 302
        assert response.location == "/login"
    email = "test@test.com"
    password = "1234"
    # When a POST request is made with an incorrect password.
    with client:
        response = client.post("/login", data={"email": email, "password": password})
        # Then the response should keep us on the login page.
        assert response.status_code == 200
        assert b"LOGIN" in response.data

def test_signup_and_invite_acceptance(client, application):
    # Test GET request to the signup page
    response = client.get('/signup')
    assert response.status_code == 200
    assert b"Register" in response.data
    test_user = UserForTests()
    name = test_user.name
    email = test_user.email
    password = test_user.password
    # Test submitting the signup form with valid credentials
    response = client.post('/signup', data={
        "name":name,
        "email":email,
        "password":password,
        "password2":password
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"LOGIN" in response.data
    # Test attempting to sign up with an already registered email
    # Test submitting the signup form with valid credentials
    response = client.post('/signup', data={
        "name":name,
        "email":email,
        "password":password,
        "password2":password
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"That email is already registered!" in response.data
    with application.app_context():
        email = test_user.email
        password = test_user.password
        from application import db
        from application.data_models import Invites, Users
        invite_unique = InviteForTests(email, 123)
        invite = Invites()
        invite.invite_id = invite_unique.invite_id
        invite.team_id = invite_unique.team_id
        db.session.add(invite)
        user = Users.query.filter_by(email=email).first()
        assert user.team_id == None
        response = client.post(f"/login/{invite.invite_id}", data={"email": email, "password": password})
        # Then the response should redirect to the home page
        assert response.status_code == 302
        assert response.location == "/"
        user = Users.query.filter_by(email=email).first()
        assert user.team_id == 123
            


def test_profile_and_logout(client):
    with client.session_transaction() as session:
        session["email"] = "123@123.com"
        session["team_id"] = 123    
        assert "email" in session
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"123@123.com" in response.data
    response = client.post("/profile", data={"submit": ""}, follow_redirects=True)
    assert response.status_code == 200
    assert b"LOGIN" in response.data
    with client.session_transaction() as session:
        assert "email" not in session