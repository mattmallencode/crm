def test_view_contact(client):
    with client.session_transaction() as session:
        session["email"] = "123@123.com"
        session["team_id"] = 123    
    response = client.get(f"/contact/contact/120312336%40umail.ucc.ie_2/activity")
    assert b"Recent Activity" in response.data

def test_meetings(client):
    with client.session_transaction() as session:
        session["email"] = "123@123.com"
        session["team_id"] = 123    
        session["google_token"] = (123,)
    response = client.get(f"/contact/120312336%40umail.ucc.ie_2/meetings")
    assert b"Schedule a meeting" in response.data
    form = {"title": "test_meeting", "description": "test_description"}
    response = client.post(f"/contact/120312336%40umail.ucc.ie_2/meetings")