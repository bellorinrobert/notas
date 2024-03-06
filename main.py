from fastapi import Depends, FastAPI,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.models.Users.listUsers import listUsers
from src.models.Users.User import fake_decode_token
from src.models.Users.User import User
from src.models.Users.User import UserInDB


app = FastAPI()

def fake_hash_password(password: str):
    return "fakehased" + password

oauth2_scheme = OAuth2PasswordBearer

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]):

    user = fake_decode_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credential",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user

async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        
        raise HTTPException(
            status_code=400, details="Inactive user")
    
    return current_user

@app.get("/")
def root():
    return {"message": "Notas api"}

@app.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):

    print (form_data)

    user_dict = listUsers.get(form_data.username)

    if not user_dict:
        raise HTTPException(
            status_code=400, 
            detail="Incorret username o password")
    
    user = UserInDB(**user_dict)
    
    hashed_password = fake_hash_password(form_data.password)

    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, 
            detail="Incorrect username or paswword")
    
    return {'access_token': user, "token_type": "bearer"}