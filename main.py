from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

# Define Pydantic model for User data with user_id
class User(BaseModel):
    user_id: int
    username: str
    password: str
    rating: int
    map_id: int
    gamemode_id: int

# JSON file to store user data
users_data = []

# Load user data from a separate JSON file
def load_users_data():
    try:
        with open("users_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save user data to a separate JSON file
def save_users_data():
    with open("users_data.json", "w") as file:
        json.dump(users_data, file)

# Define API endpoints

# User Data Load
users_data = load_users_data()

# Endpoint to create a user
@app.post("/user/")
def create_user(user: User):
    users_data.append(user.dict())
    save_users_data()
    return {"message": "User created successfully"}

# Endpoint to get all users
@app.get("/user/")
def get_all_users():
    return users_data

# Endpoint to update user data by user_id
@app.put("/user/")
def update_user(user: User):
    for i, existing_user in enumerate(users_data):
        if existing_user["user_id"] == user.user_id:
            existing_user.update(user.dict())
            save_users_data()
            return {"message": "User data updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to get a specific user by user_id
@app.get("/user/{user_id}")
def get_user_by_id(user_id: int):
    for user in users_data:
        if user["user_id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to delete a specific user by user_id
@app.delete("/user/{user_id}")
def delete_user_by_id(user_id: int):
    for user in users_data:
        if user["user_id"] == user_id:
            users_data.remove(user)
            save_users_data()
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Define Pydantic model for Map data with mapid
class Map(BaseModel):
    mapid: int
    name: str

# JSON file to store map data
maps_data = []

# Load map data from a separate JSON file
def load_maps_data():
    try:
        with open("maps_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save map data to a separate JSON file
def save_maps_data():
    with open("maps_data.json", "w") as file:
        json.dump(maps_data, file)

# Define API endpoints

# Maps Data Load
maps_data = load_maps_data()

# Endpoint to create a map
@app.post("/map/")
def create_map(map: Map):
    maps_data.append(map.dict())
    save_maps_data()
    return {"message": "Map created successfully"}

# Endpoint to get all maps
@app.get("/map/")
def get_all_maps():
    return maps_data

# Endpoint to update map data by mapid
@app.put("/map/")
def update_map(map: Map):
    for i, existing_map in enumerate(maps_data):
        if existing_map["mapid"] == map.mapid:
            existing_map.update(map.dict())
            save_maps_data()
            return {"message": "Map data updated successfully"}
    raise HTTPException(status_code=404, detail="Map not found")

# Endpoint to get a specific map by mapid
@app.get("/map/{map_id}")
def get_map_by_id(map_id: int):
    for map in maps_data:
        if map["mapid"] == map_id:
            return map
    raise HTTPException(status_code=404, detail="Map not found")

# Endpoint to delete a specific map by mapid
@app.delete("/map/{map_id}")
def delete_map_by_id(map_id: int):
    for map in maps_data:
        if map["mapid"] == map_id:
            maps_data.remove(map)
            save_maps_data()
            return {"message": "Map deleted successfully"}
    raise HTTPException(status_code=404, detail="Map not found")


# Define Pydantic model for Game Mode data with mode_id
class GameMode(BaseModel):
    mode_id: int
    name: str

# JSON file to store game mode data
gamemodes_data = []

# Load game mode data from a separate JSON file
def load_gamemodes_data():
    try:
        with open("gamemodes_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save game mode data to a separate JSON file
def save_gamemodes_data():
    with open("gamemodes_data.json", "w") as file:
        json.dump(gamemodes_data, file)

# Define API endpoints

# Data Load
gamemodes_data = load_gamemodes_data()

# Endpoint to create a game mode
@app.post("/gamemode/")
def create_gamemode(gamemode: GameMode):
    gamemodes_data.append(gamemode.dict())
    save_gamemodes_data()
    return {"message": "Game Mode created successfully"}

# Endpoint to get all game modes
@app.get("/gamemode/")
def get_all_gamemodes():
    return gamemodes_data

# Endpoint to update game mode data by mode_id
@app.put("/gamemode/")
def update_gamemode(gamemode: GameMode):
    for i, existing_gamemode in enumerate(gamemodes_data):
        if existing_gamemode["mode_id"] == gamemode.mode_id:
            existing_gamemode.update(gamemode.dict())
            save_gamemodes_data()
            return {"message": "Game Mode data updated successfully"}
    raise HTTPException(status_code=404, detail="Game Mode not found")

# Endpoint to get a specific game mode by mode_id
@app.get("/gamemode/{mode_id}")
def get_gamemode_by_id(mode_id: int):
    for gamemode in gamemodes_data:
        if gamemode["mode_id"] == mode_id:
            return gamemode
    raise HTTPException(status_code=404, detail="Game Mode not found")

# Endpoint to delete a specific game mode by mode_id
@app.delete("/gamemode/{mode_id}")
def delete_gamemode_by_id(mode_id: int):
    for gamemode in gamemodes_data:
        if gamemode["mode_id"] == mode_id:
            gamemodes_data.remove(gamemode)
            save_gamemodes_data()
            return {"message": "Game Mode deleted successfully"}
    raise HTTPException(status_code=404, detail="Game Mode not found")


# Define Pydantic model for Matchmaking request
class MatchmakingRequest(BaseModel):
    user_id: int

# Load user data from the "users_data.json" file
def load_users_data():
    try:
        with open("users_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to find matchmaking opponents
def find_matchmaking_opponents(user_id, users_data):
    # Find the user requesting matchmaking
    requesting_user = None
    for user in users_data:
        if user["user_id"] == user_id:
            requesting_user = user
            break

    if requesting_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Initialize matchmaking opponents
    matchmaking_opponents = []

    # Iterate through users to find suitable matchmaking opponents
    for user in users_data:
        if (
            user["user_id"] != requesting_user["user_id"] and
            user["map_id"] == requesting_user["map_id"] and
            user["gamemode_id"] == requesting_user["gamemode_id"]
        ):
            # Calculate the rating difference between the requesting user and potential opponent
            rating_difference = abs(requesting_user["rating"] - user["rating"])

            # Ensure that the rating difference is within a specified range (200 points)
            if rating_difference <= 200:
                matchmaking_opponents.append(user)

                # Break when there are 5 suitable opponents
                if len(matchmaking_opponents) == 5:
                    break

    if len(matchmaking_opponents) < 1:
        raise HTTPException(status_code=404, detail="Insufficient suitable opponents for matchmaking")

    return matchmaking_opponents

# Define API endpoint for matchmaking
@app.post("/matchmaking/", response_model=list[dict])
def matchmaking(request: MatchmakingRequest):
    users_data = load_users_data()
    matchmaking_opponents = find_matchmaking_opponents(request.user_id, users_data)
    return matchmaking_opponents

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)