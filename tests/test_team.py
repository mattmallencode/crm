from tests.classes_for_tests import UserForTests

def test_invite(client):
    # Log in as a user who is an admin of a team
    with client.session_transaction() as session:
        session["email"] = "123@123.com"
        session["team_id"] = 123    
    # Make a POST request to the invite route with a valid email address
    response = client.post("/invite",
        data={'email': 'test@test.com'},
        follow_redirects=True)
    assert response.status_code == 200
    assert b"Member has been invited" in response.data

def test_create_team(client):
    test_user = UserForTests()
    name = test_user.name
    email = test_user.email
    password = test_user.password

    response = client.post('/signup', data={
        "name":name,
        "email":email,
        "password":password,
        "password2":password
    }, follow_redirects=True)

    with client.session_transaction() as session:
        session["email"] = email

    # Make a POST request to the createTeam route with a valid team name
    response = client.post(
        "/create_team",
        data={'name': 'Test Team'},
        follow_redirects=True)

    assert response.status_code == 200
    assert b"You are already a member of a team" not in response.data
    assert b"Create a new team" not in response.data