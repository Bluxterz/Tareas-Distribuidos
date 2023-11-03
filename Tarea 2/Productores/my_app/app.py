from flask import Flask, request, render_template
from kafka import KafkaProducer
import json

app = Flask(__name__)

# Configura el productor Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/', methods=['GET', 'POST'])
def notificar_falta_stock():
    if request.method == 'POST':
        maestro_id = request.form['maestro_id']
        stock_agotado = request.form.get('stock_agotado', 'no') == 'si'

        # Mensaje de notificación
        notificacion = {
            'maestro_id': maestro_id,
            'stock_agotado': stock_agotado
        }

        # Nombre del tópico de Gestión de Ingredientes
        topic = 'gestion-ingredientes'

        # Envía el mensaje al tópico
        producer.send(topic, value=notificacion)

        return "Notificación enviada con éxito."

    return render_template('formulario.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
