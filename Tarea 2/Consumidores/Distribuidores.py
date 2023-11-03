from kafka import KafkaConsumer
import json
import mysql.connector

conexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='120119',
    database='tarea2distribuidos'
)


cursor = conexion.cursor()


def restablecer_stock():
    global stock_carrito
    stock_carrito = 0


restablecer_stock()


consumer = KafkaConsumer(
    'gestion-ingredientes',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)


def coordinar_reposicion(mensaje):
    global stock_carrito 
    maestro_id = mensaje['maestro_id']
    stock_agotado = mensaje['stock_agotado']

    if stock_agotado:
        stock_carrito += 10 
        print(f"Reposición de stock coordinada para el Maestro {maestro_id}. Stock del carrito aumentado a {stock_carrito}")

        
        query = "INSERT INTO StockCarrito (maestro_id, stock) VALUES (%s, %s) ON DUPLICATE KEY UPDATE stock = stock + %s"
        valores = (maestro_id, 10, 10) 
        cursor.execute(query, valores)
        conexion.commit()
    else:
        print("Stock Completo.")

for mensaje in consumer:
    mensaje_data = mensaje.value
    coordinar_reposicion(mensaje_data)

cursor.close()
conexion.close()
