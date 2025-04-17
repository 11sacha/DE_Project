# SOLVO Challenge

This project implements a real-time data processing pipeline using **Apache Flink**, **Apache Kafka**, and **Python (PyFlink)** to calculate Click-Through Rate (CTR) metrics for ad campaigns.

It simulates streaming events (ad impressions and clicks), processes them with Flink in 1-minute tumbling windows, and writes analytics results back to Kafka.

---

## ⚙️ Stack

- **Apache Kafka**: Stream ingestion
- **Apache Flink (PyFlink)**: Stream processing and windowed aggregations
- **Python**: Event simulation & processing logic
- **Docker Compose**: Service orchestration
- **Kafka UI**: Monitoring Kafka topics in real time

---

### 1. Build Docker image
```
docker compose build
```

### 2. Initialize container
```
docker compose up
```

### 3. Stop container
```
docker compose down
```

### 4. Generate data
```
python3 generate_events.py
```