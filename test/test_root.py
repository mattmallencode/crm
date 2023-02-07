from test import client
import mock
import pytest
from flask import session, request, appcontext_pushed, g, jsonify, json
from application import Users, Teams,Invites, Contacts, login_required, application

from httpx import AsyncClient
from . import init_db

def test_landing(client):
    landing = client.get("/login")
    html = landing.data.decode()
    # Test that this link is visible on the html login page.
    assert '<a class = "signup_link" href="/signup">here</a>' in html

    # Test that this page returned an OK 200 code
    assert landing.status_code == 200

# Since you have to login. If you attempt to visit the home page it will bring you to the login page.
def test_landing_aliases(client):
    landing = client.get("/home")
    assert client.get("/home").data == landing.data

'''Since the login works we are going to test the SQLAlchemy interface for the database'''
def test_user():
    # When a user is created test the parameters are handled correctly
    user = Users('oliver12345@gmail.com', None, 1, True, True)
    assert user.email == 'oliver12345@gmail.com'
    assert user.password_hash == None
    assert user.team_id == 1
    assert user.owner_status == True
    assert user.admin_status == True


def test_invites():
    invites = Invites('123456', 1)
    assert invites.invite_id == '123456'
    assert invites.team_id == 1

def test_contacts():
    contacts = Contacts('ksdkisdf', 1, 'Oliver', 'oliverksndkdfn@gmail.com', 3990003, 'Jerry', 'Dell', 'active')
    assert contacts.contact_id == 'ksdkisdf'
    assert contacts.team_id == 1
    assert contacts.name == 'Oliver'
    assert contacts.email == 'oliverksndkdfn@gmail.com'
    assert contacts.phone_number == 3990003
    assert contacts.contact_owner == 'Jerry'
    assert contacts.company == 'Dell'
    assert contacts.status == 'active'

def test_teams():
    teams = Teams(1, 'RagnBone')
    assert teams.team_id == 1
    assert teams.name == 'RagnBone'

# test that the page will redirect if the user is not logged in.
def test_login_page_not_logged_in(client):
    resource = client.get('/')
    assert resource.status_code == 302
# Test login when the page is logged in 
def test_login_page_logged_in(client):
    with client:
        client.post('/login', data=dict(email='test@gmail.com', password='test'))
        resource = client.get('/login')
        assert resource.status_code == 200

def test_sign_up(client):
    with client:    
        client.post('/signup', data=dict(email='test@gmail.com', password='test'))
        resource = client.get('signup')
        assert resource.status_code == 200

'''@pytest.yield_fixture
async def client():
    async with AsyncClient(application=application, base_url='http://localhost:8000/') as async_client:
            yield async_client

@pytest.yield_fixture
def user_to_create():
    yield UserCreate(
            email="test_client@example.com",
            username="test_client",
            password="testclientpassword"
    )
class TestAPI:

    @pytest.mark.asyncio
    async def test_user_create(self, client, init_db, user_to_create):
        response = await client.post('/', json=user_to_create.dict())
        assert response.status_code == 200
        data = response.json()
        assert data['username'] == user_to_create.username
    '''