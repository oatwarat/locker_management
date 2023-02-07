from fastapi import FastAPI, HTTPException, Body
from datetime import date
from pydantic import BaseModel
from pymongo import MongoClient

DATABASE_NAME = "hotel"
COLLECTION_NAME = "reservation"
MONGO_DB_URL = f"mongodb://exceed12:q7MRP7qp@mongo.exceed19.online"
MONGO_DB_PORT = 8443


class Management(BaseModel):
    available: str
    locker_id : int
    start_time: date
    end_time: date
    items: str
    user_id: int


client = MongoClient(f"{MONGO_DB_URL}:{MONGO_DB_PORT}")

db = client[DATABASE_NAME]

collection = db[COLLECTION_NAME]

app = FastAPI()


def locker_avaliable(locker_id: int, status: bool):
    is_avail = {"Available": status}
    result = collection.find(is_avail)
    lockers = list(result)
    if len(lockers) == 0:
        raise HTTPException(status_code=404, detail=f"No locker available right now")
    return lockers




