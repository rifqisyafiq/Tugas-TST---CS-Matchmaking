import json
from typing import List, Optional
from fastapi import APIRouter, Body, HTTPException, status, Depends
from routes.auth import get_current_user
from models.users import User

users_data = []

user_router = APIRouter(tags=["User"])

with open("data/users_data.json", "r") as file:
    users_data = json.load(file)

@user_router.get("/user/")
def get_all_users(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return users_data
    else:
        # If not admin, only return the current user's profile
        return [user for user in users_data if user["user_id"] == current_user.user_id]

@user_router.get("/user/{user_id}")
def get_user_by_id(user_id: int, current_user: User = Depends(get_current_user)):
    for user in users_data:
        if user["user_id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@user_router.post("/user/")
def create_user(user: User, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        users_data.append(user.dict())
        with open("data/users_data.json", "w") as file:
            json.dump(users_data, file)
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden. Only admin can create users.")

@user_router.put("/user/")
def update_user(user: User, current_user: User = Depends(get_current_user)):
    if current_user.is_admin or user.user_id == current_user.user_id:
        for i, existing_user in enumerate(users_data):
            if existing_user["user_id"] == user.user_id:
                existing_user.update(user.dict())
                with open("data/users_data.json", "w") as file:
                    json.dump(users_data, file)
                return {"message": "User data updated successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Forbidden. You can only update your own profile or as an admin.")

@user_router.delete("/user/{user_id}")
def delete_user_by_id(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.is_admin or user_id == current_user.user_id:
        for user in users_data:
            if user["user_id"] == user_id:
                users_data.remove(user)
                with open("data/users_data.json", "w") as file:
                    json.dump(users_data, file)
                return {"message": "User deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Forbidden. You can only delete your own profile or as an admin.")
