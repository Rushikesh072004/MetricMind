from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.database import initialize_database

from src.analytics import (
    get_total_value,
    get_average_value,
    get_value_by_category,
    get_business_profit,
    get_business_insight,
    get_trend_data,
    get_anomalies,
    get_areas_to_improve,
)

from src.semantic_layer import (
    answer_query,
    get_metric_value,
    get_all_metrics,
    calculate_profit_margin,
)


# ============================================================
# DATABASE
# ============================================================

initialize_database()


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="MetricMind API",
    description=(
        "MetricMind is a business analytics and "
        "conversational business intelligence platform."
    ),
    version="2.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# FRONTEND
# ============================================================

app.mount(
    "/dashboard",
    StaticFiles(
        directory="data/api/config/frontend",
        html=True,
    ),
    name="dashboard",
)


# ============================================================
# REQUEST MODELS
# ============================================================

class QueryRequest(BaseModel):
    query: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return RedirectResponse(url="/dashboard/")


# ============================================================
# API STATUS
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MetricMind API",
        "version": "2.0.0",
    }


@app.get("/api/status")
def api_status():
    return {
        "status": "online",
        "service": "MetricMind API",
        "version": "2.0.0",
    }


# ============================================================
# METRICS
# ============================================================

@app.get("/metrics")
def get_metrics():

    metrics = get_all_metrics()

    revenue = metrics.get("revenue", 0)
    cost = metrics.get("cost", 0)
    sales = metrics.get("sales", 0)

    profit = revenue - cost

    return {
        "sales": sales,
        "revenue": revenue,
        "cost": cost,
        "profit": profit,
        "profit_margin": calculate_profit_margin(),
    }


# ============================================================
# ANALYTICS
# ============================================================

@app.get("/analytics")
def analytics():

    category_results = get_value_by_category()

    categories = {}

    for category, value in category_results:
        if category:
            categories[category.lower()] = value or 0

    return {
        "total_value": get_total_value(),
        "average_value": get_average_value(),
        "business_profit": get_business_profit(),
        "profit_margin": calculate_profit_margin(),
        "categories": categories,
        "business_insight": get_business_insight(),
    }


# ============================================================
# TREND
# ============================================================

@app.get("/trend")
def trend():

    return {
        "trend": get_trend_data()
    }


# ============================================================
# ANOMALIES
# ============================================================

@app.get("/anomalies")
def anomalies():

    return {
        "anomalies": get_anomalies()
    }


# ============================================================
# IMPROVEMENTS
# ============================================================

@app.get("/improvements")
def improvements():

    return {
        "improvements": get_areas_to_improve()
    }


# ============================================================
# QUERY ASSISTANT
# ============================================================

@app.post("/query")
def query_metric(request: QueryRequest):

    query = request.query.strip()

    if not query:
        return {
            "query": "",
            "answer": "Please enter a business question.",
        }

    result = answer_query(query)

    return {
        "query": query,
        "answer": result,
    }


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

@app.get("/dashboard-data")
def dashboard_data():

    metrics = get_all_metrics()

    revenue = metrics.get("revenue", 0)
    cost = metrics.get("cost", 0)

    return {
        "metrics": {
            "sales": metrics.get("sales", 0),
            "revenue": revenue,
            "cost": cost,
            "profit": revenue - cost,
            "profit_margin": calculate_profit_margin(),
        },
        "analytics": {
            "total_value": get_total_value(),
            "average_value": get_average_value(),
            "business_profit": get_business_profit(),
        },
        "trend": get_trend_data(),
        "anomalies": get_anomalies(),
        "improvements": get_areas_to_improve(),
        "business_insight": get_business_insight(),
    }


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )