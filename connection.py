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
        if __name__=='__main__':
            print("Connection to the database was successful.")
            print(connection)
        return connection
    except Exception as e:
        print(str(e))
