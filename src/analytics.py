from src.database import get_connection


# ============================================================
# BASIC ANALYTICS
# ============================================================

def get_total_value():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(value), 0)
        FROM metrics
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


def get_value_by_category():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, COALESCE(SUM(value), 0)
        FROM metrics
        GROUP BY category
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_average_value():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(AVG(value), 0)
        FROM metrics
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


# ============================================================
# BUSINESS PROFIT
# ============================================================

def get_business_profit():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN LOWER(category) = 'revenue'
                        THEN value
                        ELSE 0
                    END
                ), 0
            )
            -
            COALESCE(
                SUM(
                    CASE
                        WHEN LOWER(category) = 'cost'
                        THEN value
                        ELSE 0
                    END
                ), 0
            )
        FROM metrics
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


# ============================================================
# BUSINESS INSIGHT
# ============================================================

def get_business_insight():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN LOWER(category) = 'revenue'
                        THEN value
                        ELSE 0
                    END
                ), 0
            ),
            COALESCE(
                SUM(
                    CASE
                        WHEN LOWER(category) = 'cost'
                        THEN value
                        ELSE 0
                    END
                ), 0
            )
        FROM metrics
    """)

    revenue, cost = cursor.fetchone()

    connection.close()

    revenue = revenue or 0
    cost = cost or 0

    profit = revenue - cost

    if revenue == 0:
        return "No revenue data is currently available."

    margin = (profit / revenue) * 100

    if profit < 0:
        return (
            f"Business is operating at a loss of "
            f"{abs(profit):,.2f}. Cost control should be prioritized."
        )

    if margin < 10:
        return (
            f"Business is profitable, but the profit margin is low "
            f"at {margin:.2f}%. Consider improving pricing or reducing costs."
        )

    if margin < 20:
        return (
            f"Business is profitable with a {margin:.2f}% profit margin. "
            f"There is room to improve operational efficiency."
        )

    return (
        f"Business is performing well with a "
        f"{margin:.2f}% profit margin."
    )


# ============================================================
# TREND ANALYSIS
# ============================================================

def get_trend_data():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            strftime('%Y-%m', created_at) AS month,

            SUM(
                CASE
                    WHEN LOWER(category) = 'revenue'
                    THEN value
                    ELSE 0
                END
            ) AS revenue,

            SUM(
                CASE
                    WHEN LOWER(category) = 'cost'
                    THEN value
                    ELSE 0
                END
            ) AS cost

        FROM metrics

        GROUP BY month

        ORDER BY month
    """)

    results = cursor.fetchall()

    connection.close()

    trend = []

    for month, revenue, cost in results:

        revenue = revenue or 0
        cost = cost or 0

        trend.append({
            "month": month,
            "revenue": revenue,
            "cost": cost,
            "profit": revenue - cost,
        })

    return trend


# ============================================================
# ANOMALY DETECTION
# ============================================================

def get_anomalies():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            value,
            category,
            created_at
        FROM metrics
        ORDER BY value
    """)

    results = cursor.fetchall()

    connection.close()

    if len(results) < 3:
        return []

    values = [row[2] for row in results]

    average = sum(values) / len(values)

    if average == 0:
        return []

    anomalies = []

    for row in results:

        metric_id, name, value, category, created_at = row

        if value > average * 2:

            anomalies.append({
                "id": metric_id,
                "name": name,
                "value": value,
                "category": category,
                "created_at": created_at,
                "type": "Unusually High",
                "severity": "high",
                "message": (
                    "This value is significantly above "
                    "the normal metric level."
                ),
            })

        elif value < average * 0.5:

            anomalies.append({
                "id": metric_id,
                "name": name,
                "value": value,
                "category": category,
                "created_at": created_at,
                "type": "Unusually Low",
                "severity": "medium",
                "message": (
                    "This value is significantly below "
                    "the normal metric level."
                ),
            })

    return anomalies


# ============================================================
# AREAS TO IMPROVE
# ============================================================

def get_areas_to_improve():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            LOWER(category),
            COALESCE(SUM(value), 0)
        FROM metrics
        GROUP BY LOWER(category)
    """)

    results = cursor.fetchall()

    connection.close()

    category_values = {
        category: value
        for category, value in results
        if category
    }

    revenue = category_values.get("revenue", 0)
    cost = category_values.get("cost", 0)
    sales = category_values.get("sales", 0)

    improvements = []

    if revenue <= 0:

        improvements.append({
            "title": "Increase Revenue",
            "priority": "High",
            "reason": "Revenue data is currently zero or unavailable.",
            "action": "Focus on revenue-generating activities and customer acquisition.",
        })

    if revenue > 0:

        profit = revenue - cost
        margin = (profit / revenue) * 100

        if cost > revenue:

            improvements.append({
                "title": "Reduce Operating Costs",
                "priority": "High",
                "reason": "Operating costs are higher than revenue.",
                "action": "Review major cost drivers and identify unnecessary expenses.",
            })

        elif cost > revenue * 0.5:

            improvements.append({
                "title": "Improve Cost Control",
                "priority": "Medium",
                "reason": "Costs consume more than half of revenue.",
                "action": "Review recurring expenses and improve operational efficiency.",
            })

        if margin < 20:

            improvements.append({
                "title": "Improve Profit Margin",
                "priority": "Medium",
                "reason": f"Current profit margin is {margin:.2f}%.",
                "action": "Consider pricing optimization or cost reduction.",
            })

    if sales <= 0:

        improvements.append({
            "title": "Increase Sales",
            "priority": "High",
            "reason": "Sales data is currently zero or unavailable.",
            "action": "Focus on customer acquisition and sales conversion.",
        })

    if not improvements:

        improvements.append({
            "title": "Maintain Performance",
            "priority": "Low",
            "reason": "Current business indicators are healthy.",
            "action": "Continue monitoring KPIs and maintain operational discipline.",
        })

    return improvements


# ============================================================
# TERMINAL ANALYTICS
# ============================================================

def show_analytics():

    print("\n================================")
    print("       MetricMind Analytics")
    print("================================")

    print(
        f"Total Value: "
        f"{get_total_value():,.2f}"
    )

    print(
        f"Average Value: "
        f"{get_average_value():,.2f}"
    )

    print(
        f"Business Profit: "
        f"{get_business_profit():,.2f}"
    )

    print("\nValue by Category:")

    for category, value in get_value_by_category():

        print(
            f"- {category}: {value:,.2f}"
        )

    print("\nBusiness Insight:")

    print(get_business_insight())

    print("\nAreas to Improve:")

    for area in get_areas_to_improve():

        print(
            f"- {area['title']} "
            f"({area['priority']})"
        )


if __name__ == "__main__":
    show_analytics()