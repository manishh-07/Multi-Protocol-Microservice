FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN python -m grpc_tools.protoc -I./app/protos --python_out=./app/generated --grpc_python_out=./app/generated app/protos/health.proto
RUN sed -i 's/^import health_pb2/from . import health_pb2/' app/generated/health_pb2_grpc.py

EXPOSE 8080
RUN adduser --disabled-password --gecos '' appuser
USER appuser

CMD ["python", "app/main.py"]