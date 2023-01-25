from application import Users

def test_user():
    """ 
    Given a user 
    Check when a user is created,
    Check the email, hashed_password
    """
    user = Users('oliverlinger@gmail.com', 123454, 1, True, True)
    assert user.email == 'oliverlinger@gmail.com'
    assert user.password_hash != '123454'
    assert user.team_id == 1
    assert user.owner_status == True
    assert user.admin_status == True

