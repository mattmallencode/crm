from test import client


def test_landing(client):
    landing = client.get("/")
    html = landing.data.decode()

    # Check that links to `about` and `login` pages exist
    assert " <a href=\"/signup/\">signup</a>" in html


    assert landing.status_code == 200


def test_landing_aliases(client):
    landing = client.get("/")
    assert client.get("/index/").data == landing.data