import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('LOCAL_USER')}:"
    f"{os.getenv('LOCAL_PASSWORD')}@postgres:5432/"
    f"{os.getenv('LOCAL_DB')}"
)

def get_connection():
    return psycopg.connect(DATABASE_URL)


def viewGameRooms():
    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute("SELECT * FROM gameRooms")

            rows = cursor.fetchall()

            print("\n========== GAME ROOMS ==========")

            for row in rows:
                print(f"Room Name: {row[0]}")
                print(f"Player Names: {row[1]}")
                print("--------------------------------")

            print(f"Total rooms: {len(rows)}")


if __name__ == "__main__":
    viewGameRooms()

    