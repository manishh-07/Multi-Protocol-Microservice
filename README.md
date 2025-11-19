# Multi-Protocol Health Microservice (POC)

## 🚀 Overview

This project is a Proof of Concept (POC) for a modern, high-performance microservice architecture used within the Eros Universe ecosystem. It demonstrates how to serve multiple communication protocols from a single application instance:

1.  **REST API (FastAPI):** For standard external communication and Kubernetes Probes.
2.  **gRPC (grpc.aio):** For high-speed, low-latency Backend-to-Backend (B2B) communication.
3.  **SSE (Server-Sent Events):** For real-time status updates to the Frontend.

## 🎯 Purpose

* **Standardization:** Provides a template for future microservices requiring mixed protocols.
* **Resilience:** Implements graceful shutdown patterns to handle Kubernetes scaling events without dropping connections.
* **Observability:** Exposes dedicated Liveness and Readiness probes for Kubernetes.

## 📂 Folder Structure

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
│   ├── protos/                 # Proto Source Files (.proto)
│   └── generated/              # Auto-generated gRPC code (Ignored in Git)
├── Dockerfile                  # Multi-stage build
├── requirements.txt            # Python dependencies
└── README.md
```

### Prerequisites
---
- Python 3.11+

- Docker

- pip and virtualenv

### Local Development Setup
---
1. Environment Setup
Create a virtual environment and install dependencies.

```bash
# Create virtual env
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate
# Activate (Windows)
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
2. Environment Variables
Create a .env file in the root directory:

```ini, TOML
APP_ENVIRONMENT=dev
REST_PORT=8080
GRPC_PORT=50051
SSE_INTERVAL=5
APP_DEBUG=True
```
3. Generate gRPC Stubs (Crucial Step)
Before running the app, you must generate the Python code from the .proto files.

```bash
# Run from the root directory
python -m grpc_tools.protoc -I./app/protos --python_out=./app/generated --grpc_python_out=./app/generated app/protos/health.proto

# Fix relative import issue (Mac/Linux)
sed -i 's/^import health_pb2/from . import health_pb2/' app/generated/health_pb2_grpc.py
```
4. Run the Application
```bash
python -m app.main
```
- REST Server starts on http://0.0.0.0:8080

- gRPC Server starts on 0.0.0.0:50051

### Docker Build & Run
---
To verify the application in a containerized environment:

```bash
# Build the image
docker build -t health-poc:latest .

# Run the container (Mapping both ports)
docker run --rm -p 8080:8080 -p 50051:50051 health-poc:latest
```

### Testing & Verification
---
1. **REST Health Check (External/K8s)**
```bash
curl http://localhost:8080/api/health-poc/health
```
**Expected Response**: {"status":"operational","is_healthy":true...}

2. **Server-Sent Events (Frontend Real-time)**
```bash
curl -N http://localhost:8080/api/health-poc/events
```
**Expected Response**: Continuous stream of data every 5 seconds.

3. **gRPC Check (Internal Backend)**
You can use a python script or grpcurl to test the socket connection.

**Python Socket Test:**

```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('localhost', 50051))
print("Port Open" if result == 0 else "Port Closed")
sock.close()
```
### Deployment (Helm)
* This project is deployed via ArgoCD using the charts-rest-grpc-sse Helm chart.

* Key Configuration (values.yaml):

    - Service: Exposes ports 8080 (http) and 50051 (grpc).

    - Gateway: Configured with HTTPRoute on path /api/health-poc.

    - Probes: Custom paths set to /api/health-poc/health.

    ```bash
    # Example internal DNS usage (from another pod)
    curl http://charts-rest-grpc-sse-test.charts-rest-grpc-sse-test:8080/api/health-poc/health
    ```
