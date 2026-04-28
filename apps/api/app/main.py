import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("migration-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Database Migration Hub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/portfolio")
def get_portfolio():
    return [
        {"id": "mig-fin-001", "name": "Oracle to Postgres", "source": "Oracle 19c", "target": "Azure Database for PG", "status": "SYNCING", "progress": 82},
        {"id": "mig-hr-042", "name": "SQL Server Modernization", "source": "SQL 2012", "target": "SQL Managed Instance", "status": "VALIDATING", "progress": 95},
        {"id": "mig-sales-101", "name": "MySQL to Aurora", "source": "MySQL 5.7", "target": "AWS Aurora MySQL", "status": "COMPLETED", "progress": 100}
    ]

@app.get("/assessments/summary")
def get_assessment_summary():
    return {
        "total_instances": 142,
        "ready_for_migration": 84,
        "high_risk_instances": 12,
        "avg_complexity_score": 74
    }

@app.get("/waves/summary")
def get_waves_summary():
    return {
        "active_waves": 3,
        "next_cutover": "2026-05-15",
        "total_db_size": "452 TB",
        "avg_sync_lag": "1.2s"
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_successful_migrations": 245,
        "cost_savings_est": "$2.4M",
        "hypercare_incidents": 2,
        "avg_downtime_mins": 5
    }

@app.post("/assessments/run")
def run_assessment(instance_id: str, target_engine: str):
    logger.info(f"Triggering assessment for {instance_id} towards {target_engine}")
    return {"status": "Assessment Job Enqueued", "job_id": "job_assess_123"}

@app.post("/migrations/run")
def run_migration(instance_id: str, wave_id: str):
    logger.info(f"Triggering migration for {instance_id} in wave {wave_id}")
    return {"status": "Migration Job Enqueued", "job_id": "job_mig_456"}
