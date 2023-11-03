from flask import Flask, request, render_template
from kafka import KafkaProducer
import json
import mysql.connector  

app = Flask(__name__)

#Configuracion kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Configuracion MySQL
config_mysql = {
    'user': 'root',
    'password': '120119',
    'host': 'localhost',
    'database': 'tarea2distribuidos'
}

@app.route('/', methods=['GET', 'POST'])
def notificar_falta_stock():
    if request.method == 'POST':
        maestro_id = request.form['maestro_id']
        stock_agotado = request.form.get('stock_agotado', 'no') == 'si'

        notificacion = {
            'maestro_id': maestro_id,
            'stock_agotado': stock_agotado
        }

        topic = 'gestion-ingredientes'

        producer.send(topic, value=notificacion)

        return "Notificación enviada con éxito."

    ids_inscripciones = obtener_ids_inscripciones()

    return render_template('formulario.html', ids_inscripciones=ids_inscripciones)

def obtener_ids_inscripciones():
    db_connection = mysql.connector.connect(**config_mysql)
    cursor = db_connection.cursor()
    
    cursor.execute('SELECT id FROM inscripciones')
    ids_inscripciones = [row[0] for row in cursor.fetchall()]

    cursor.close()
    db_connection.close()

    return ids_inscripciones

if __name__ == '__main__':
    app.debug = True
    app.run()
