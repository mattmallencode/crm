import pytest
from application import create_app

@pytest.fixture()
def application():
    application = create_app()
    application.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield application

    # clean up / reset resources here

@pytest.fixture()
def client(application):
    return application.test_client()


@pytest.fixture()
def runner(application):
    return application.test_cli_runner()

@pytest.fixture()
def user(client):
    # Set up session variables for authenticated user
        with client.session_transaction() as session:
            session['email'] = 'test@test.com'
            session['team_id'] = 123