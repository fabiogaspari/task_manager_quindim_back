class UserResponse:
    id: str
    username: str
    email: str

    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}