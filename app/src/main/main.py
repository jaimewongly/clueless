print("Starting PostgreSQL setup...")

from src.database.connection import connect, disconnect



def main():
    connection = connect()
    if connection:
        print("Database connection established.")
        # Here you can add logic to execute queries or commands
        cur = connection.cursor()
        cur.execute("SELECT version();")
        print(cur.fetchone())
        cur.close()
        disconnect(connection)
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()