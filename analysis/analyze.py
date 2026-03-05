import csv
import statistics

latencies = []
stale_count = 0
total_get = 0

with open("../results/metrics.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["op"] == "GET":
            total_get += 1
            latencies.append(float(row["latency_ms"]))
            stale_count += int(row["stale"])

if total_get == 0:
    print("No GET operations recorded.")
    exit()

avg_latency = sum(latencies) / len(latencies)
p95_latency = sorted(latencies)[int(0.95 * len(latencies))]
stale_rate = stale_count / total_get

print("Total GETs:", total_get)
print("Average Latency (ms):", round(avg_latency, 3))
print("P95 Latency (ms):", round(p95_latency, 3))
print("Stale Read Rate:", round(stale_rate, 4))
