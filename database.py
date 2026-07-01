import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def get_connection():
    """
    Returns a database connection.

    Usage:
        with get_connection() as conn:
            result = conn.execute(text("SELECT * FROM employees"))
    """
    return engine.connect()

def test_connection():
    """
    Tests whether the database connection is working.
    """
    try:
        with get_connection() as conn:

            result = conn.execute(text("SELECT NOW();"))

            current_time = result.scalar()

            print("=" * 50)
            print("Connected Successfully!")
            print("Database Time:", current_time)
            print("=" * 50)

    except Exception as e:
        print("=" * 50)
        print("Connection Failed")
        print(e)
        print("=" * 50)


if __name__ == "__main__":
    test_connection()
