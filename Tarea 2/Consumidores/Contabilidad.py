from confluent_kafka import Consumer, KafkaError
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector

# Conectar a la base de datos MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='120119',
    database='tarea2distribuidos'
)
cursor = conn.cursor()

config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-contabilidad',
    'auto.offset.reset': 'earliest'
}

consumidor_contabilidad = Consumer(config)

tópico_ventas = 'ventas'

# Función para enviar correo con estadísticas
def enviar_correo_estadisticas(montehusillero_id, total_ventas_semana, ganancias_semana):
    servidor_smtp = 'smtp.gmail.com'  
    puerto_smtp = 587  
    usuario = 'matias.guzman.g.2001@gmail.com'  
    contraseña = 'ywek iwdp qsmz tbzd' 

    # Realiza una consulta para obtener los datos del montehusillero desde la base de datos
    cursor.execute('''
        SELECT correo, nombre, apellido FROM inscripciones WHERE id = %s
    ''', (montehusillero_id,))
    resultado = cursor.fetchone()

    if resultado:
        destinatario = resultado[0]
        nombre = resultado[1]
        apellido = resultado[2]

        mensaje = MIMEMultipart()
        mensaje['From'] = usuario
        mensaje['To'] = destinatario
        mensaje['Subject'] = 'Estadísticas de ventas semanales'

        mensaje_texto = f'''
        Estadísticas de ventas semanales:

        Montehusillero: {nombre} {apellido}
        Cantidad de ventas realizadas esta semana: {len(total_ventas_semana)}
        Ganancias semanales: ${ganancias_semana}
        Ventas semanales: {", ".join(map(str, total_ventas_semana))}
        '''
        mensaje.attach(MIMEText(mensaje_texto, 'plain'))

        try:
            servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
            servidor.starttls()
            servidor.login(usuario, contraseña)
            servidor.sendmail(usuario, destinatario, mensaje.as_string())
            servidor.quit()
            print(f'Correo electrónico enviado al Montehusillero ID {montehusillero_id}')
        except Exception as e:
            print('Error al enviar el correo electrónico:', str(e))

ventas_semana = {}
n_ventas_para_correo = 7

while True:
    mensaje = consumidor_contabilidad.poll(1.0)
    if mensaje is None:
        continue
    if mensaje.error():
        if mensaje.error().code() == KafkaError._PARTITION_EOF:
            # Realiza un seguimiento de ventas semanales para cada montehusillero
            for montehusillero_id, (ventas_semana, ganancias_semana) in ventas_semana.items():
                if len(ventas_semana) >= n_ventas_para_correo:
                    enviar_correo_estadisticas(montehusillero_id, ventas_semana, ganancias_semana)
                # Reinicia el seguimiento para esta semana
                ventas_semana[montehusillero_id] = ([], 0)
        else:
            print('Error en el mensaje: {}'.format(mensaje.error()))
    else:
        # Procesa el mensaje de venta
        venta = json.loads(mensaje.value())
        montehusillero_id = venta['montehusillero_id']
        ventas_semana_actual = venta['ventas_semana']

        # Realiza un seguimiento de ventas semanales para el montehusillero
        total_ventas_semana, ganancias_semana = ventas_semana.get(montehusillero_id, ([], 0))
        total_ventas_semana.extend(ventas_semana_actual)
        ganancias_semana += sum(ventas_semana_actual)
        ventas_semana[montehusillero_id] = (total_ventas_semana, ganancias_semana)

        # Muestra información con cada venta
        print(f'Datos de venta recibidos para Montehusillero ID {montehusillero_id}')
