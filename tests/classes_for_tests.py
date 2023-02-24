from uuid import uuid4
from secrets import token_urlsafe

class UserForTests:
    def __init__(self):
        self.name = "Test User"
        self.email = f"{uuid4()}@{uuid4()}.com"
        self.password = "password"

class InviteForTests:
    def __init__(self, email, team_id):
        self.team_id = team_id
        self.invite_id = f"{email}_{team_id}_{token_urlsafe(16)}"