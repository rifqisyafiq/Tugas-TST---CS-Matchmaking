from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
import jwt
import json
from models.users import Token, UserIn, User

# Load user data from JSON file
with open("data/users_data.json", "r") as json_file:
    users_data = json.load(json_file)

auth_router = APIRouter(tags=["Authentication"])
JWT_SECRET = 'myjwtsecret'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# Function to write user data to JSON file
def write_users_to_json():
    with open("data/users_data.json", "w") as json_file:
        json.dump(users_data, json_file, indent=4)

# Function to authenticate and get user
def authenticate_user(username: str, password: str):
    for user in users_data:
        if user['username'] == username and bcrypt.verify(password, user['hashed_password']):
            return user
    return user

# OAuth2 password bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# Route to generate token
@auth_router.post('/token', response_model=Token)
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    token_data = {"sub": user['username'], "user_id": user['user_id']}
    token = jwt.encode(token_data, JWT_SECRET)

    return {'access_token': token, 'token_type': 'bearer'}

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = payload.get('user_id')
        user = next((u for u in users_data if u['user_id'] == user_id), None)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Invalid user'
            )
        return User(**user)  # Convert user dictionary to User Pydantic model
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid token'
        )

# Route to get current user
@auth_router.get('/users/me', response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user

# Route to register a new user
@auth_router.post('/register', response_model=User)
async def register_user(user: UserIn):
    user_id = len(users_data) + 1
    password_hash = bcrypt.hash(user.password)
    
    is_admin = False
    if user.username == "admin":
        is_admin = True
        
    new_user = {"user_id": user_id, "username": user.username, "password_hash": password_hash, "rating" : user.rating, "map_id" : user.map_id,
                "gamemode_id" : user.gamemode_id, "is_admin": is_admin}
 
    users_data.append(new_user)
    write_users_to_json()
    return new_user