from pydantic import BaseModel

# Pydantic model for user registration
class UserIn(BaseModel):
    username: str
    password: str
    rating: int
    map_id: int
    gamemode_id: int

# Pydantic model for token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Pydantic model for user data in JSON file
class User(BaseModel):
    user_id: int
    username: str
    hashed_password: str
    rating: int
    map_id: int
    gamemode_id: int
    is_admin : bool