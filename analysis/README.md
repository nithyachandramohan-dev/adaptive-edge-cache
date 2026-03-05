# Adaptive TTL and Version-Check Consistency for Distributed Edge Caching

## Overview
This project implements a distributed edge caching system with:

- 1 Origin server
- 3 Edge nodes
- Version-based validation
- Adaptive TTL strategy
- Experimental workload generator

The system evaluates the trade-off between latency and stale-read probability under varying write intensities.

## Architecture
Client → Edge Nodes → Origin Server

## Technologies
- Python (FastAPI)
- Docker & Docker Compose
- Git
- Distributed Systems concepts (TTL, Versioning, Bounded Staleness)

## Experiments
Evaluated under write probabilities:
- 0.01
- 0.1
- 0.3

Metrics collected:
- Average latency
- P95 latency
- Stale-read rate

## How to Run

```bash
docker compose build
docker compose up
