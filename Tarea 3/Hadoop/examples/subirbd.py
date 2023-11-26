import json
import mysql.connector

def mysql_connect():
    try:
        connection = mysql.connector.connect(
            host='mysql',
            user='root',
            password='db',
            database='tarea3'
        )
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)
        raise

def load_json_to_mysql(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    connection = mysql_connect()
    cursor = connection.cursor()

    try:
        for word, values in data.items():
            for document, count in values.items():
                query = "INSERT INTO paginas (palabras, documento, frecuencia) VALUES (%s, %s, %s)"
                cursor.execute(query, (word, document, count))

        connection.commit()

    except mysql.connector.Error as err:
        print("Error during MySQL operation:", err)

    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    json_file_path = "./database/db.json"
    load_json_to_mysql(json_file_path)
