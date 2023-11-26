import mysql.connector
import json

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

def search_word_in_mysql(word):
    # Configuración de la conexión MySQL
   
    # Crear la conexión MySQL
    mysql_conn = mysql_connect()

    # Crear un cursor
    cursor = mysql_conn.cursor(dictionary=True)

    # Ejecutar la consulta para buscar la palabra en la tabla
    query = f"SELECT documento, frecuencia FROM paginas WHERE palabras = '{word}' ORDER BY Frecuencia;"
    cursor.execute(query)

    # Obtener los resultados
    results = cursor.fetchall()

    # Cerrar cursor y conexión
    cursor.close()
    mysql_conn.close()

    return results

def get_url_for_document(document):
    # Leer el contenido del archivo urls.txt
    with open('./urls.txt', 'r') as urls_file:
        for line in urls_file:
            doc_num, url = line.strip().split(" ", 1)
            if doc_num == document:
                return url

    return ''

def main():
    user_input = input("Buscar Palabra: ")

    top_results = search_word_in_mysql(user_input)

    # Agregar la URL correspondiente a cada resultado
    for result in top_results:
        result['url'] = get_url_for_document(result['documento'])

    formatted_results = json.dumps({user_input: top_results}, indent=2, ensure_ascii=False)
    print(formatted_results)

if __name__ == "__main__":
    main()
