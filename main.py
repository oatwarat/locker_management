from fastapi import FastAPI, HTTPException, Body

from datetime import date, datetime, timedelta

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


def locker_available(status: bool):
    lst_unavail = []
    lst_avail = []
    if status:
        for locker in collection.find({"available": status}):
            lst_avail.append({
                "available": True,
                "locker_id": locker["locker_id"]
            })
        return lst_avail

    current_date_and_time = datetime.now()
    for locker in collection.find({"available": status}):
        time = datetime.strptime(locker["end_time"], '%Y-%m-%d %H:%M:%S') - current_date_and_time
        lst_unavail.append({
            "available": False,
            "locker_id": locker["locker_id"],
            "remaining_time": time.seconds
        })

    return lst_unavail


def reserve_locker(locker_id: int, items: list, time: date, status: bool, user_id: int):
    if len(items) == 0:
        raise HTTPException(status_code=400, detail=f"You cannot deposit 0 items in the locker.")

    if time > datetime.now() + timedelta(hours=2):
        extra_hours = (time - (datetime.now() + timedelta(hours=2))).total_seconds() / 3600
        cost = 5 * int(extra_hours)
        return f"You will have to pay an additional {cost} Baht for depositing the items for more than 2 hours."

    collection.update_one({'locker_id': locker_id},
                          {'$set': {"items": items, "user_id": user_id, "end_time": time, "Available": False}})
    return "Locker reservation successful."


def return_locker(student_id: int, locker_id: int, amount_paid: float):
    locker = collection.find_one({"locker_id": locker_id})
    if locker is None:
        raise HTTPException(status_code=404, detail=f"Locker with id {locker_id} not found.")
    if locker["user_id"] != student_id:
        raise HTTPException(status_code=401, detail="Unauthorized access.")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(locker["end_time"], "%Y-%m-%d %H:%M:%S")
    time_diff = (end_time - datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")).total_seconds() / 60
    extra_charge = 0
    if time_diff > 120:
        extra_time = time_diff - 120
        extra_charge = (extra_time // 10) * 20
    if amount_paid < extra_charge:
        raise HTTPException(status_code=400,
                            detail=f"Insufficient payment. {extra_charge - amount_paid} baht is still owed.")

    change = amount_paid - extra_charge

    collection.update_one({"locker_id": locker_id}, {
        "$set": {"available": True, "user_id": None, "items": [], "start_time": None, "end_time": None}})

    return {"change": change}



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

