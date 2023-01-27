from test import client


def test_landing(client):
    landing = client.get("/login")
    html = landing.data.decode()
    
    assert " <a href=\"/signup/\">signup</a>" in html


    assert landing.status_code == 200


'''def test_landing_aliases(client):
    landing = client.get("/")
    assert client.get("/").data == landing.data'''