import sqlite3

from src.database import DB_PATH


def seed_historical_data():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Historical business data
    historical_data = [

        # May 2026
        ("May Revenue", 120000, "revenue", "2026-05-15 10:00:00"),
        ("May Cost", 60000, "cost", "2026-05-15 10:05:00"),
        ("May Sales", 150000, "sales", "2026-05-15 10:10:00"),

        # June 2026
        ("June Revenue", 140000, "revenue", "2026-06-15 10:00:00"),
        ("June Cost", 70000, "cost", "2026-06-15 10:05:00"),
        ("June Sales", 180000, "sales", "2026-06-15 10:10:00"),

        # July 2026
        ("July Revenue", 165000, "revenue", "2026-07-15 10:00:00"),
        ("July Cost", 75000, "cost", "2026-07-15 10:05:00"),
        ("July Sales", 210000, "sales", "2026-07-15 10:10:00"),

        # August 2026
        ("August Revenue", 180000, "revenue", "2026-08-15 10:00:00"),
        ("August Cost", 65000, "cost", "2026-08-15 10:05:00"),
        ("August Sales", 300000, "sales", "2026-08-15 10:10:00"),
    ]

    cursor.executemany(
        """
        INSERT INTO metrics
        (name, value, category, created_at)
        VALUES (?, ?, ?, ?)
        """,
        historical_data
    )

    connection.commit()
    connection.close()

    print("Historical data seeded successfully!")


if __name__ == "__main__":
    seed_historical_data()