from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import time
import threading
import os

app = FastAPI()

ORIGIN = os.getenv("ORIGIN_URL", "http://origin:8000")

lock = threading.Lock()
cache = {}
client = httpx.Client()

class PutReq(BaseModel):
    value: str

@app.get("/kv/{key}")
def get_kv(key: str):
    now = time.time()

    with lock:
        if key in cache and now < cache[key]["expiry"]:
            return {
                "value": cache[key]["value"],
                "version": cache[key]["version"],
                "source": "cache"
            }

    origin_version = client.get(f"{ORIGIN}/version/{key}").json()["version"]

    with lock:
        if key in cache and cache[key]["version"] == origin_version:
            cache[key]["expiry"] = now + 5
            return {
                "value": cache[key]["value"],
                "version": cache[key]["version"],
                "source": "validated"
            }

    data = client.get(f"{ORIGIN}/kv/{key}").json()

    with lock:
        cache[key] = {
            "value": data["value"],
            "version": data["version"],
            "expiry": now + 5
        }

    return {
        "value": data["value"],
        "version": data["version"],
        "source": "refreshed"
    }

@app.put("/kv/{key}")
def put_kv(key: str, req: PutReq):
    data = client.put(f"{ORIGIN}/kv/{key}", json={"value": req.value}).json()

    with lock:
        cache[key] = {
            "value": data["value"],
            "version": data["version"],
            "expiry": time.time() + 5
        }

    return data
