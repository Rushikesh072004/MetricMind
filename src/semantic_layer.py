from src.database import get_connection


# ============================================================
# METRIC DEFINITIONS
# ============================================================

METRICS = {
    "sales": "Sales",
    "revenue": "Revenue",
    "cost": "Cost",
}


# ============================================================
# GET METRIC
# ============================================================

def get_metric_value(metric_name):

    metric_name = metric_name.lower().strip()

    if metric_name not in METRICS:
        return None

    category = METRICS[metric_name]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(value), 0)
        FROM metrics
        WHERE LOWER(category) = LOWER(?)
        """,
        (category,),
    )

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


# ============================================================
# ALL METRICS
# ============================================================

def get_all_metrics():

    return {
        "sales": get_metric_value("sales"),
        "revenue": get_metric_value("revenue"),
        "cost": get_metric_value("cost"),
    }


# ============================================================
# PROFIT
# ============================================================

def calculate_profit():

    revenue = get_metric_value("revenue")
    cost = get_metric_value("cost")

    return revenue - cost


# ============================================================
# PROFIT MARGIN
# ============================================================

def calculate_profit_margin():

    revenue = get_metric_value("revenue")
    profit = calculate_profit()

    if revenue == 0:
        return 0

    return (profit / revenue) * 100


# ============================================================
# AVERAGE
# ============================================================

def calculate_average():

    metrics = get_all_metrics()

    values = [
        value
        for value in metrics.values()
        if value is not None
    ]

    if not values:
        return 0

    return sum(values) / len(values)


# ============================================================
# HIGHEST METRIC
# ============================================================

def get_highest_metric():

    metrics = get_all_metrics()

    highest_metric = max(
        metrics,
        key=metrics.get,
    )

    return highest_metric, metrics[highest_metric]


# ============================================================
# REVENUE VS COST
# ============================================================

def get_revenue_cost_difference():

    revenue = get_metric_value("revenue")
    cost = get_metric_value("cost")

    return revenue - cost


# ============================================================
# BUSINESS HEALTH
# ============================================================

def get_business_health():

    revenue = get_metric_value("revenue")
    cost = get_metric_value("cost")
    profit = calculate_profit()
    margin = calculate_profit_margin()

    if profit > 0 and margin >= 20:
        status = "Healthy"

    elif profit > 0:
        status = "Profitable but needs improvement"

    else:
        status = "Needs attention"

    return {
        "status": status,
        "revenue": revenue,
        "cost": cost,
        "profit": profit,
        "profit_margin": margin,
    }


# ============================================================
# QUERY INSIGHTS
# ============================================================

def get_profit_insight(profit, margin):

    if profit <= 0:
        return (
            "The business is currently not generating a positive profit. "
            "Cost control and revenue improvement should be prioritized."
        )

    if margin >= 50:
        return (
            "The business is generating a strong profit margin, "
            "indicating healthy profitability."
        )

    if margin >= 20:
        return (
            "The business is profitable with a healthy margin, "
            "although continued cost monitoring is recommended."
        )

    return (
        "The business is profitable, but the relatively low margin "
        "suggests that cost optimization could improve profitability."
    )


def get_cost_insight(cost, revenue):

    if revenue == 0:
        return "Revenue data is unavailable for cost comparison."

    cost_percentage = (cost / revenue) * 100

    if cost_percentage > 70:
        return (
            f"Cost represents {cost_percentage:.1f}% of revenue. "
            "Cost optimization should be a high priority."
        )

    if cost_percentage > 50:
        return (
            f"Cost represents {cost_percentage:.1f}% of revenue. "
            "Operating expenses should be monitored closely."
        )

    return (
        f"Cost represents {cost_percentage:.1f}% of revenue, "
        "which indicates relatively controlled spending."
    )


# ============================================================
# QUERY ASSISTANT
# ============================================================

def answer_query(query):

    query = query.lower().strip()

    if not query:
        return "Please enter a business question."


    # ========================================================
    # BUSINESS SUMMARY
    # ========================================================

    if (
        "business summary" in query
        or "business overview" in query
        or query == "summary"
        or "give me a summary" in query
        or "summarize the business" in query
    ):

        sales = get_metric_value("sales")
        revenue = get_metric_value("revenue")
        cost = get_metric_value("cost")
        profit = calculate_profit()
        margin = calculate_profit_margin()

        insight = get_profit_insight(profit, margin)

        return (
            "📊 BUSINESS SUMMARY\n\n"
            f"Sales: ₹{sales:,.2f}\n"
            f"Revenue: ₹{revenue:,.2f}\n"
            f"Cost: ₹{cost:,.2f}\n"
            f"Profit: ₹{profit:,.2f}\n"
            f"Profit Margin: {margin:.2f}%\n\n"
            f"💡 Insight: {insight}"
        )


    # ========================================================
    # BUSINESS HEALTH / PERFORMANCE
    # ========================================================

    if (
        "business health" in query
        or "business performance" in query
        or "is the business healthy" in query
        or "how is the business doing" in query
        or "how is the business performing" in query
        or "business doing" in query
        or "business performing" in query
    ):

        health = get_business_health()

        insight = get_profit_insight(
            health["profit"],
            health["profit_margin"],
        )

        return (
            "📈 BUSINESS PERFORMANCE\n\n"
            f"Status: {health['status']}\n"
            f"Revenue: ₹{health['revenue']:,.2f}\n"
            f"Cost: ₹{health['cost']:,.2f}\n"
            f"Profit: ₹{health['profit']:,.2f}\n"
            f"Profit Margin: {health['profit_margin']:.2f}%\n\n"
            f"💡 Insight: {insight}"
        )


    # ========================================================
    # PROFIT MARGIN
    # ========================================================

    if (
        "profit margin" in query
        or query == "margin"
        or "what is the margin" in query
    ):

        margin = calculate_profit_margin()
        profit = calculate_profit()

        insight = get_profit_insight(profit, margin)

        return (
            "📊 PROFIT MARGIN\n\n"
            f"Current Profit Margin: {margin:.2f}%\n\n"
            f"💡 Insight: {insight}"
        )


    # ========================================================
    # PROFIT
    # ========================================================

    if (
        "business profit" in query
        or "net profit" in query
        or query == "profit"
        or "what is the profit" in query
        or "how much profit" in query
    ):

        profit = calculate_profit()
        margin = calculate_profit_margin()

        insight = get_profit_insight(profit, margin)

        return (
            "💰 PROFIT ANALYSIS\n\n"
            f"Business Profit: ₹{profit:,.2f}\n"
            f"Profit Margin: {margin:.2f}%\n\n"
            f"💡 Insight: {insight}"
        )


    # ========================================================
    # HIGHEST METRIC
    # ========================================================

    if (
        "highest metric" in query
        or "highest value" in query
        or "largest metric" in query
        or "which metric is highest" in query
        or "highest" in query
    ):

        metric, value = get_highest_metric()

        return (
            "🏆 HIGHEST METRIC\n\n"
            f"{metric.title()} has the highest value at "
            f"₹{value:,.2f}.\n\n"
            "💡 Insight: This is currently the largest "
            "recorded metric among sales, revenue, and cost."
        )


    # ========================================================
    # REVENUE VS COST
    # ========================================================

    if (
        "revenue vs cost" in query
        or "revenue compared to cost" in query
        or "difference between revenue and cost" in query
        or "compare revenue and cost" in query
    ):

        revenue = get_metric_value("revenue")
        cost = get_metric_value("cost")
        difference = revenue - cost

        if difference >= 0:

            return (
                "⚖️ REVENUE VS COST\n\n"
                f"Revenue: ₹{revenue:,.2f}\n"
                f"Cost: ₹{cost:,.2f}\n"
                f"Difference: ₹{difference:,.2f}\n\n"
                "💡 Insight: Revenue is higher than cost, "
                "resulting in a positive operating difference."
            )

        return (
            "⚠️ REVENUE VS COST\n\n"
            f"Revenue: ₹{revenue:,.2f}\n"
            f"Cost: ₹{cost:,.2f}\n"
            f"Difference: ₹{abs(difference):,.2f}\n\n"
            "💡 Insight: Cost is higher than revenue and "
            "requires immediate attention."
        )


    # ========================================================
    # AVERAGE
    # ========================================================

    if (
        "average" in query
        or "average metric" in query
    ):

        average = calculate_average()

        return (
            "📊 AVERAGE METRIC\n\n"
            f"Average Metric Value: ₹{average:,.2f}\n\n"
            "💡 Insight: This represents the average value "
            "across the available business metrics."
        )


    # ========================================================
    # SALES
    # ========================================================

    if (
        "sales" in query
        or "what are the sales" in query
        or "what is the sales" in query
        or "how much sales" in query
    ):

        sales = get_metric_value("sales")

        return (
            "🛒 SALES ANALYSIS\n\n"
            f"Total Sales: ₹{sales:,.2f}\n\n"
            "💡 Insight: This represents the total recorded "
            "sales value in the business database."
        )


    # ========================================================
    # REVENUE
    # ========================================================

    if (
        "revenue" in query
        or "what is the revenue" in query
        or "how much revenue" in query
    ):

        revenue = get_metric_value("revenue")
        cost = get_metric_value("cost")

        return (
            "💵 REVENUE ANALYSIS\n\n"
            f"Total Revenue: ₹{revenue:,.2f}\n\n"
            f"💡 Insight: {get_cost_insight(cost, revenue)}"
        )


    # ========================================================
    # COST
    # ========================================================

    if (
        "cost" in query
        or "what is the cost" in query
        or "how much cost" in query
    ):

        cost = get_metric_value("cost")
        revenue = get_metric_value("revenue")

        return (
            "💸 COST ANALYSIS\n\n"
            f"Total Cost: ₹{cost:,.2f}\n\n"
            f"💡 Insight: {get_cost_insight(cost, revenue)}"
        )


    # ========================================================
    # UNKNOWN QUESTION
    # ========================================================

    return (
        "I couldn't identify that business question.\n\n"
        "You can ask me about:\n"
        "• Sales\n"
        "• Revenue\n"
        "• Cost\n"
        "• Profit\n"
        "• Profit margin\n"
        "• Average metric\n"
        "• Highest metric\n"
        "• Revenue vs cost\n"
        "• Business summary\n"
        "• Business health"
    )


# ============================================================
# TERMINAL HELPER
# ============================================================

def show_metric(metric_name):

    value = get_metric_value(metric_name)

    if value is None:

        print(
            f"Metric '{metric_name}' not found."
        )

    else:

        print(
            f"{metric_name.title()}: ₹{value:,.2f}"
        )