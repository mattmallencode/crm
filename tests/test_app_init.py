from flask import session, g
import json
import urllib

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