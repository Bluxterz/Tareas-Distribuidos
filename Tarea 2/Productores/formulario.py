from confluent_kafka import Producer, KafkaError
import json

# Configuración del productor
config = {
    'bootstrap.servers': 'localhost:9092',  # Cambia esto según la dirección de tu servidor Kafka
    'client.id': 'productor-inscripcion'
}

# Crear una instancia del productor
productor = Producer(config)

# Tópico al que enviarás los formularios de inscripción
tópico_inscripcion = 'formulario-inscripcion'

# Función para enviar el formulario de inscripción a Kafka
def enviar_formulario_inscripcion(formulario, es_pagado=False):
    # Añade la clave 'estado_pago' al formulario
    formulario['estado_pago'] = 'PAID' if es_pagado else 'Not Paid'
    
    # Convierte el formulario a formato JSON
    datos_formulario = json.dumps(formulario)
    
    # Envía el formulario al tópico correspondiente
    productor.produce(
        topic=tópico_inscripcion,
        key=None,
        value=datos_formulario,

        callback=delivery_report
    )

# Función de entrega de mensaje para monitoreo
def delivery_report(err, msg):
    if err is not None:
        print('Mensaje no entregado: {}'.format(msg.value()))
        print('Error: {}'.format(err))
    else:
        print('Mensaje entregado a {} [{}]'.format(msg.topic(), msg.partition()))

# Ejemplo de uso para ingresar manualmente los datos del formulario
nombre = input("Nombre: ")
apellido = input("Apellido: ")
correo = input("Correo: ")
usuario = input("Usuario: ")
contraseña = input("Contraseña: ")

formulario_maestro = {
    'nombre': nombre,
    'apellido': apellido,
    'correo': correo,
    'usuario': usuario,
    'contraseña': contraseña
}

# Solicita si es un formulario "PAID"
es_pagado = input("¿Es un formulario PAID? (Sí/No): ").strip().lower() == "sí"
# Envía el formulario al tópico de inscripción
enviar_formulario_inscripcion(formulario_maestro, es_pagado)
# Espera a que todos los mensajes se envíen (puedes personalizar este tiempo)
productor.flush()
