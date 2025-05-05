from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from pymongo import MongoClient
from bson import ObjectId
import uvicorn
import zlib
from fastapi.staticfiles import StaticFiles
from bson.binary import Binary
from fastapi import Body
import base64
import os
from dotenv import load_dotenv

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Load env variables
load_dotenv()
# MongoDB Connection (sync)
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
# client = MongoClient("mongodb+srv://alfredsam2006:iu0rXT9uUTbPxj5B@cluster0.62cl52u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


# db = client["akshaya"]
song_collection = db["songs"]
user_collection = db["user_logs"]

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = user_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="🚫 User not found. Please sign up first.")

    if user["password"] != password:
        raise HTTPException(status_code=401, detail="❌ Invalid credentials. Please check your password.")
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "✅ Login successful",
            "user": {
                "email": user["email"]
            }
        })
    

    
@app.delete("/delete_user/{email}")
def delete_user(email: str):
    # Find the user in the database
    user = user_collection.find_one({"email": email})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete user data and their associated songs
    user_collection.delete_one({"email": email})
    song_collection.delete_many({"email": email})

    return JSONResponse(status_code=200, content={"status": "✅ User account deleted successfully"})

@app.post("/signup")
def signup(email: str = Form(...), password: str = Form(...)):
    # Check if the user already exists
    if user_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="User already exists")

    # Create new user entry
    user_data = {
        "email": email,
        "password": password
    }
    
    user_collection.insert_one(user_data)

    return JSONResponse(status_code=201, content={"status": "✅ User registered successfully"})


@app.get("/get_songs/{email}")
def get_songs(email: str):
    # Fetch songs and convert to list
    songs_cursor = song_collection.find({"email": email})
    songs = list(songs_cursor)

    # If no songs found
    if len(songs) == 0:
        raise HTTPException(status_code=404, detail="No songs found for the given email")
    
    # Format the result
    song_list = []
    for song in songs:

        mp3_data = song.get("MP3")
        d_mp3_data = zlib.decompress(mp3_data)
        mp3_base64 = base64.b64encode(d_mp3_data).decode("utf-8") if d_mp3_data else None

        song_data = {
            "song ID":str(song.get("_id")),
            "Song Name": song.get("Song Name"),
            "Artist Name": song.get("Artist Name"),
            "MP3":mp3_base64,
            "filename": song.get("filename"),
            "content_type": song.get("content_type")
        }
        song_list.append(song_data)
    
    return JSONResponse(status_code=200, content={"songs": song_list})


@app.delete("/delete_songs")
def delete_songs(song_ids: List[str] = Body(...)):
    # Convert string IDs to ObjectId
    song_ids = [ObjectId(id) for id in song_ids]
    
    result = song_collection.delete_many({"_id": {"$in": song_ids}})
    
    if result.deleted_count > 0:
        return JSONResponse(status_code=200, content={"status": f"✅ {result.deleted_count} songs deleted"})
    else:
        raise HTTPException(status_code=404, detail="No songs found with given IDs")
    

@app.put("/update_song/{song_id}")
def update_song(song_id: str, Song_Name: str = Form(...), Artist_Name: str = Form(...)):


    # Convert string ID to ObjectId
    song_id = ObjectId(song_id)
    
    song = song_collection.find_one({"_id": song_id})
    
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Update the song data
    updated_song = {
        "Song Name": Song_Name,
        "Artist Name": Artist_Name
    }

    song_collection.update_one({"_id": song_id}, {"$set": updated_song})

    return JSONResponse(status_code=200, content={"status": "✅ Song updated successfully"})



@app.post("/upload")
def upload_songs(
    email: str = Form(...),
    Song_Names: list[str] = Form(...),
    Artist_Names: list[str] = Form(...),
    MP3s: list[UploadFile] = File(...)
):

    # Prepare all documents
    songs_data = []
    for i in range(len(MP3s)):
        raw_data = MP3s[i].file.read()
        compressed_data = zlib.compress(raw_data, level=9) 
        song_data = {
            "email": email,
            "Song Name": Song_Names[i],
            "Artist Name": Artist_Names[i],
            "MP3": compressed_data,
            "filename": MP3s[i].filename,
            "content_type": MP3s[i].content_type
        }
        songs_data.append(song_data)

    # Bulk insert into MongoDB
    result = song_collection.insert_many(songs_data)

    return JSONResponse(
        status_code=200,
        content={
            "status": "✅ Bulk upload successful",
            "inserted_ids": [str(_id) for _id in result.inserted_ids]
        }
    )




# Uvicorn entrypoint
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
