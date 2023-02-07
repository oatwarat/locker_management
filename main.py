from fastapi import FastAPI, HTTPException, Body
from datetime import date, datetime
from pydantic import BaseModel
from pymongo import MongoClient

DATABASE_NAME = "hotel"
COLLECTION_NAME = "reservation"
MONGO_DB_URL = f"mongodb://exceed12:q7MRP7qp@mongo.exceed19.online"
MONGO_DB_PORT = 8443


class Management(BaseModel):
    available: bool
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
    lst_unavail = []
    lst_avail = []
    if not status:
        lst_unavail.append(collection.find({"Available" : status}))
    else:
        lst_avail.append(collection.find({"Available": status}))
    current_date_and_time = datetime.now()


    collection
    for locker in lst_unavail:
        time = datetime.strptime(end_time) - datetime.strptime(current_date_and_time)
        return time




def put_items(locker_id, items):
    if len(items) == 0:
        raise HTTPException(status_code=404, detail=f"You cannot put 0 item in locker")
    collection.update_one({'locker_id': locker_id}, {'$set': {"items": items}})




