import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="bedrocks.tplinkdns.com",
            database="StudentCabinetCurs",
            user="root",
            password="Amazon321123"
        )
        return connection

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
