from pymongo import MongoClient
import unittest
import requests

IP = "127.0.0.1"
PORT = "8000"

DATABASE_NAME = "hotel"
COLLECTION_NAME = "reservation"
MONGO_DB_URL = f"mongodb://exceed12:q7MRP7qp@mongo.exceed19.online"
MONGO_DB_PORT = 8443

BASE_URL = f"http://{IP}:{PORT}"


def connect_mongodb():
    client = MongoClient(f"{MONGO_DB_URL}:{MONGO_DB_PORT}")
    global db;
    db = client[DATABASE_NAME]
    global collection;
    collection = db[COLLECTION_NAME]

    collection.delete_many({})

    print("MongoClient connected\n")
