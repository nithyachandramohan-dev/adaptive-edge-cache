import time
import random
import csv
import httpx
import os

ORIGIN = "http://origin:8000"
EDGES = [
    "http://edge1:8001",
    "http://edge2:8001",
    "http://edge3:8001"
]

DURATION = 20
WRITE_PROB = 0.3
N_KEYS = 50

client = httpx.Client(timeout=5.0)

# Make sure directory exists
os.makedirs("/results", exist_ok=True)

file_path = "/results/metrics.csv"

print("Writing results to:", file_path)

with open(file_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["op", "key", "latency_ms", "stale"])

    start = time.time()
    i = 0

    while time.time() - start < DURATION:
        key = f"k{random.randint(0, N_KEYS)}"
        edge = EDGES[i % len(EDGES)]
        t0 = time.time()

        try:
            if random.random() < WRITE_PROB:
                client.put(f"{edge}/kv/{key}", json={"value": str(random.randint(0,10000))})
            else:
                r = client.get(f"{edge}/kv/{key}")
                data = r.json()
                origin_version = client.get(f"{ORIGIN}/version/{key}").json()["version"]
                stale = 1 if data["version"] < origin_version else 0
                writer.writerow(["GET", key, (time.time()-t0)*1000, stale])
        except Exception as e:
            print("Request error:", e)

        i += 1
        time.sleep(0.01)

print("Finished workload successfully")
time.sleep(5)
