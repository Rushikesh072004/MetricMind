# MetricMind 📊

### Business Analytics & Conversational BI Platform

MetricMind is a business analytics and conversational Business Intelligence (BI) platform built with Python, FastAPI, SQLite, HTML, CSS, and JavaScript.

It helps users monitor business metrics, analyze revenue and costs, identify unusual values, generate actionable recommendations, visualize business trends, and ask business questions using a natural-language Query Assistant.

---

## 🚀 Features

- 📊 Interactive business dashboard
- 💰 Sales, revenue, and cost monitoring
- 📈 Profit and profit-margin analysis
- 📉 Monthly revenue, cost, and profit trends
- 🚨 Business anomaly detection
- 💡 Actionable business recommendations
- 🤖 Natural-language Query Assistant
- ❤️ Business health analysis
- 🔌 REST APIs using FastAPI
- 🟢 API health/status monitoring
- 📱 Responsive dashboard interface

---

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### Database
- SQLite
- SQL

### Testing & Development
- Python Virtual Environment
- VS Code
- Git
- GitHub

---

## 🏗️ Architecture

```text
                    User
                      ↓
              MetricMind Dashboard
                HTML / CSS / JS
                      ↓
                 FastAPI API
                      ↓
        ┌─────────────┴─────────────┐
        ↓                           ↓
 Analytics Layer              Semantic Layer
        ↓                           ↓
        └─────────────┬─────────────┘
                      ↓
               SQLite Database
                      ↓
              Business Insights
📂 Project Structure
MetricMind/
│
├── data/
│   └── api/
│       └── config/
│           └── frontend/
│               └── index.html
│
├── sc/
│   └── seed.py
│
├── src/
│   ├── analytics.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   └── semantic_layer.py
│
├── tests/
│   └── test_semantic_layer.py
│
├── .gitignore
├── requirements.txt
└── README.md

📊 Analytics

MetricMind calculates important business indicators including:

Total business value
Average metric value
Revenue
Cost
Business profit
Profit margin
Category-wise values
Business performance insights
Profit
Profit = Revenue - Cost
Profit Margin
Profit Margin = (Profit / Revenue) × 100
🚨 Anomaly Detection

MetricMind analyzes business metric values and identifies unusually high or low values.

Detected anomalies include:

Metric name
Metric value
Category
Date
Anomaly type

This helps users quickly identify business data that may require attention.

💡 Actionable Recommendations

The system analyzes business performance and generates recommendations based on the available metrics.

Examples include:

Increase revenue generation
Reduce operating costs
Improve cost control
Improve profit margin
Focus on increasing sales
Maintain healthy business performance
🤖 Query Assistant

MetricMind includes a natural-language business Query Assistant.

Example questions:

What is the revenue?

What is the cost?

What is the profit?

What is the profit margin?

How is the business performing?

Give me a business summary.

Which metric is highest?

Compare revenue and cost.

What is the average metric value?

The Semantic Layer interprets supported business questions and returns the corresponding business information.

🔌 API Endpoints
Method	Endpoint	Purpose
GET	/health	API health check
GET	/api/status	API status
GET	/metrics	Business metrics
GET	/analytics	Business analytics
GET	/trend	Business trends
GET	/anomalies	Detected anomalies
GET	/improvements	Business recommendations
GET	/dashboard-data	Combined dashboard data
POST	/query	Query Assistant
▶️ How to Run
1. Clone the repository
git clone https://github.com/Rushikesh072004/MetricMind.git
cd MetricMind
2. Create a virtual environment
python -m venv .venv
3. Activate the virtual environment

Windows:

.venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Start the application
uvicorn src.main:app --reload
6. Open the dashboard
http://127.0.0.1:8000/dashboard/
7. Open API documentation
http://127.0.0.1:8000/docs
🖥️ Dashboard

The MetricMind dashboard provides a centralized view of:

Key Performance Indicators
Revenue and cost
Profit and margin
Business trends
Anomalies
Recommendations
Query Assistant
API status
🎯 Project Objective

The goal of MetricMind is to demonstrate how business data can be transformed into useful insights through:

Business Data
      ↓
SQLite Database
      ↓
SQL + Python Analytics
      ↓
FastAPI REST APIs
      ↓
Interactive Dashboard
      ↓
Insights + Anomalies
      ↓
Recommendations
      ↓
Conversational Query Assistant
🔮 Future Enhancements

Potential future improvements include:

User authentication
Role-based access control
Cloud database integration
Advanced machine-learning anomaly detection
Predictive forecasting
Automated business reports
PDF/Excel report export
Additional business data sources
Cloud deployment
👨‍💻 Project Status

Completed — Portfolio Ready

MetricMind currently provides a functional business analytics dashboard, REST API layer, analytics engine, anomaly detection, actionable recommendations, and conversational business query functionality.

📄 License

This project is intended for educational, portfolio, and demonstration purposes.
