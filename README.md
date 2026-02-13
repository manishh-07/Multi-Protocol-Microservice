# Multi-Protocol Health Microservice (Health Monitor) (develop branch)

## Overview

This project is a Proof of Concept (POC) for a modern, high-performance microservice architecture used within the Eros Universe ecosystem. It functions as a **Central Health Monitor** that serves multiple communication protocols:

1.  **REST API (FastAPI):** For standard self-health checks (Kubernetes Probes).
2.  **gRPC (grpc.aio):** Acts as a **Client** to connect internally to Backend Services (like `EU-Geo`) for high-speed checks, and as a **Server** for upstream checks.
3.  **SSE (Server-Sent Events):** Streams real-time status updates of downstream services (e.g., Geo) to the Frontend.

## Purpose

* **Centralized Monitoring:** Polls internal services via gRPC and aggregates status.
* **Resilience:** Implements "Graceful Degradation" — The Monitor stays alive even if target services are down.
* **Real-Time Observability:** Pushes live health data to dashboards without polling.

## Folder Structure

```text
eros-health-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point (Lifespan manager)
│   ├── api/                    # Interface Layer
│   │   ├── rest/               # REST & SSE Routers
│   │   └── grpc/               # gRPC Servicers
│   ├── core/                   # Config (Pydantic) & Settings
│   ├── services/               # Business Logic Layer
│   │   ├── __init__.py
│   │   └── health_checker.py   # gRPC Client Logic (Calls EU-Geo)
│   ├── protos/                 # Proto Source Files (.proto)
│   └── generated/              # Auto-generated gRPC code (Ignored in Git)
├── Dockerfile                  # Multi-stage build
├── requirements.txt            # Python dependencies
└── README.md
```
## Prerequisites
---
- Python 3.11+
- Docker
- pip and virtualenv

## Local Development Setup
---
1. Environment Setup
Create a virtual environment and install dependencies.

```bash
# Create virtual env
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Environment Variables
Create a .env file in the root directory:

```ini, TOML
APP_ENVIRONMENT=dev
APP_DEBUG=True

# Network Config
REST_PORT=8080
GRPC_PORT=50051
SSE_INTERVAL=5

# Monitoring Target (Geo Service Address)
# Format: <service-name>.<namespace>:<port>
GEO_GRPC_TARGET=localhost:50051
```

## Generate gRPC Stubs (Crucial Step) 
Before running the app, you must generate the Python code from the .proto files.
```bash
# Run from the root directory
python -m grpc_tools.protoc -I./app/protos --python_out=./app/generated --grpc_python_out=./app/generated app/protos/health.proto

# Fix relative import issue (Mac/Linux)
sed -i 's/^import health_pb2/from . import health_pb2/' app/generated/health_pb2_grpc.py
```
## Run the Application

```Bash
python -m app.main
```
- REST Server starts on http://0.0.0.0:8080
- gRPC Server starts on 0.0.0.0:50051
---
## Testing & Verification
Self Health Check (External/K8s) This endpoint checks if the Monitor App itself is running. It does not call downstream services.

```Bash
curl http://localhost:8080/api/health-poc/health
```
- Expected Response: ```bash{"status":"operational", "service": "Health-Monitor"}```

Real-Time Monitoring (SSE) This endpoint connects to the Geo Service via gRPC and streams its status.

```Bash
curl -N http://localhost:8080/api/health-poc/events
```

- Expected Response:
```bash
data: {
  "monitor_target": "EU-Geo Service",
  "status": "operational",
  "remote_component": "EU-Geo-Service",
  "connection": "gRPC Connected"
}
```
gRPC Port Check (Internal Backend) Verifies that this service is also reachable via gRPC.

---
