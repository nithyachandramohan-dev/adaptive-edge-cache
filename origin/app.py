from fastapi import FastAPI
from pydantic import BaseModel
import threading

app = FastAPI()

lock = threading.Lock()
store = {}

class PutReq(BaseModel):
    value: str

@app.get("/kv/{key}")
def get_kv(key: str):
    with lock:
        if key not in store:
            store[key] = {"value": "", "version": 0}
        return store[key]

@app.get("/version/{key}")
def get_version(key: str):
    with lock:
        if key not in store:
            store[key] = {"value": "", "version": 0}
        return {"version": store[key]["version"]}

@app.put("/kv/{key}")
def put_kv(key: str, req: PutReq):
    with lock:
        if key not in store:
            store[key] = {"value": "", "version": 0}
        store[key]["version"] += 1
        store[key]["value"] = req.value
        return store[key]
