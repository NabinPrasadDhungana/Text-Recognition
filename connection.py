import psycopg

def get_connection():
    try:
        connection = psycopg.connect(
            dbname="scan_doc",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
