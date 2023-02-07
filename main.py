from fastapi import FastAPI, HTTPException, Body
from datetime import datetime
from pydantic import BaseModel
from pymongo import MongoClient

DATABASE_NAME = "exceed12"
COLLECTION_NAME = "locker_management"
MONGO_DB_URL = f"mongodb://exceed12:q7MRP7qp@mongo.exceed19.online:8443/?authMechanism=DEFAULT"
MONGO_DB_PORT = 8443


class Management(BaseModel):
    available: bool
    locker_id: int
    start_time: datetime
    end_time: datetime
    items: list
    user_id: int


client = MongoClient(f"{MONGO_DB_URL}")

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


@app.post("/reserve_locker")
def reserve(management: Management):
    start_time = management.start_time
    end_time = management.end_time
    l_id = management.locker_id
    if start_time > end_time:
        raise HTTPException(status_code=400, detail="Reservation can not be made")
    if l_id < 1 or l_id > 6:
        raise HTTPException(status_code=400, detail="Reservation can not be made")
    #if locker not available
    #   raise HTTPException(status_code=400, detail="Reservation can not be made")
    query = {
        "available": bool(management.available),
        "locker_id": l_id,
        "start_time": start_time,
        "end_time": end_time,
        "items": management.items,
        "user_id": int(management.user_id)
    }
    collection.update_one(query, {f"$set": query}, upsert=True)
    return {
        "available": bool(management.available),
        "locker_id": l_id,
        "start_time": start_time,
        "end_time": end_time,
        "items": management.items,
        "user_id": management.user_id
    }

@app.delete("/reserve_locker/delete/{locker_id}/{start_time}")
def delete_reservation(locker_id: int, start_time: datetime):
    collection.delete_one({"locker_id": locker_id, "start_time": start_time})
    return "removed a reservation from locker " + str(locker_id)
