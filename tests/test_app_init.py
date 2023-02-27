from flask import session, g

class MockResponse:

    def __init__(self, data):
        self.data = data

def test_load_logged_in_user(client):
    with client:
        # Set up session variables for authenticated userz
        with client.session_transaction() as session:
            session['email'] = 'test@test.com'
            session['team_id'] = 123
        
        # Make a request to a protected endpoint
        response = client.get('/')

        # Assert that the decorator function correctly set g.email and g.team_id
        assert response.status_code == 200
        assert g.email == 'test@test.com'
        assert g.team_id == 123

def test_authorize_email(client, monkeypatch):
    # Mock the google.authorize() function to return a redirect URL
    redirect_url = b"/authorize_email/authorized/"
    monkeypatch.setattr("flask_oauthlib.client.OAuthRemoteApp.authorize", lambda self, callback: redirect_url)
    with client:
        response = client.get("/authorize_email/123")
        assert session["contact_id_redirect"] == "123"
        # Assert that the response is a redirect to the Google authorization page
        assert response.status_code == 200
        assert response.data == redirect_url 

def test_authorized(client, monkeypatch):
    user = MockResponse({"email": "test@test.com"})
    monkeypatch.setattr("flask_oauthlib.client.OAuthRemoteApp.get", lambda self, userinfo: user)
    with client:
        with client.session_transaction() as session:
            session["contact_id_redirect"] = 123
            access_token = {"access_token": 123}
        response = client.post("/authorize_email/authorized/", json=access_token)
        with client.session_transaction() as session:
            assert response.status_code == 302
            assert "contact_id_redirect" not in session
            assert session["user_google"] == "test@test.com"
            assert session["google_token"] == (123,)

def test_save_timezone(client, user):
    # User is a fixture that logs in a user for testing.
    with client:
        response = client.post('/save_timezone', data={'time_zone': 'Europe/Dublin'})
        assert response.status_code == 204
        assert session['time_zone'] == 'Europe/Dublin'