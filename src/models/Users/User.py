from pydantic import BaseModel


from .listUsers import listUsers

class User(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    
    hashed_password: str

def get_user(db, username: str):
    
    if username in db:
        
        user_dict = db[username]

        return UserInDB(**user_dict)
    
def fake_decode_token(token):
    
    user = get_user(listUsers, token)

    return user

