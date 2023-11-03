from confluent_kafka import Producer, KafkaError
import json

config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'productor-ventas'
}


productor = Producer(config)

topico_ventas = 'ventas'

# Función para enviar datos de venta
def enviar_venta(montehusillero_id, ventas_semana):
    venta = {
        'montehusillero_id': montehusillero_id,
        'ventas_semana': ventas_semana
    }
    ventas_json = json.dumps(venta)

    def delivery_report(err, msg):
        if err is not None:
            print('Error al enviar mensaje: {}'.format(err))
        else:
            print('Mensaje enviado a {} [{}]'.format(msg.topic(), msg.partition()))

    productor.produce(
        topic=topico_ventas,
        key=None,
        value=ventas_json,
        callback=delivery_report
    )
    productor.flush()

# Solicitar entrada del usuario para ingresar datos de venta
montehusillero_id = int(input("Ingresa la ID del montehusillero: "))
ventas_semana = []
for i in range(7):
    monto = float(input(f"Ingrese el monto de la venta {i+1} de la semana: $"))
    ventas_semana.append(monto)

enviar_venta(montehusillero_id, ventas_semana)
print(f'Datos de ventas enviados para Montehusillero ID {montehusillero_id}')
