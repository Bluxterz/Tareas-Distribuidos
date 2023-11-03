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

# Crear una tabla para almacenar las inscripciones si no existe
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inscripciones (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255),
        apellido VARCHAR(255),
        usuario VARCHAR(255),
        contraseña VARCHAR(255),
        correo VARCHAR(255)
    )
''')
conn.commit()

# Configuración del consumidor para el proceso de aprobación
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-aprobacion',
    'auto.offset.reset': 'earliest'
}
consumidor_aprobacion = Consumer(config)

# Tópico de Kafka para las inscripciones
tópico_inscripcion = 'formulario-inscripcion'
tópico_pago = 'formulario-inscripcion-paid'  

# Suscribir al tópico de inscripciones y al tópico de formularios pagados
consumidor_aprobacion.subscribe([tópico_inscripcion, tópico_pago])

# Función para enviar correo electrónico cuando se aprueba una inscripción
def enviar_correo_aprobacion(formulario):
    # Configura los datos del servidor de correo electrónico
    servidor_smtp = 'smtp.gmail.com'  
    puerto_smtp = 587  
    usuario = 'matias.guzman.g.2001@gmail.com'  
    contraseña = 'ywek iwdp qsmz tbzd' 

    destinatario = formulario['correo']  #

    
    mensaje = MIMEMultipart()
    mensaje['From'] = usuario
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Credenciales para MAMOCHI'

    # Contenido del correo
    mensaje_texto = f'''
    Hola {formulario['nombre']} {formulario['apellido']},

    Gracias por tu inscripción en MAMOCHI. Aquí están tus credenciales de acceso:

    Usuario: {formulario['usuario']}
    Contraseña: {formulario['contraseña']}

    Utiliza estas credenciales para acceder a tu cuenta y hacer valer tus beneficios.

    ¡Bienvenido a MAMOCHI!

    Atentamente,
    El equipo de MAMOCHI
    '''
    mensaje.attach(MIMEText(mensaje_texto, 'plain'))

    # Conéctate al servidor de correo y envía el mensaje
    try:
        servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
        servidor.starttls()
        servidor.login(usuario, contraseña)
        servidor.sendmail(usuario, destinatario, mensaje.as_string())
        servidor.quit()
        print('Correo electrónico enviado con éxito')
    except Exception as e:
        print('Error al enviar el correo electrónico:', str(e))


while True:
    mensaje = consumidor_aprobacion.poll(1.0)
    if mensaje is None:
        continue
    if mensaje.error():
        if mensaje.error().code() == KafkaError._PARTITION_EOF:
            print('Fin de la partición, continuando...')
        else:
            print('Error en el mensaje: {}'.format(mensaje.error()))
    else:
        # Verificar desde qué tópico proviene el mensaje
        tópico = mensaje.topic()
        datos_inscripcion = json.loads(mensaje.value())  # Decodificar los datos JSON
        
        if tópico == tópico_inscripcion:
            # Gestionar la inscripción estándar
            print('Inscripción aprobada (estándar): {}'.format(datos_inscripcion))
            # Llamar a la función para enviar correo electrónico
            enviar_correo_aprobacion(datos_inscripcion)

            # Insertar los datos en la base de datos
            cursor.execute('''
                INSERT INTO inscripciones (nombre, apellido, usuario, contraseña, correo)
                VALUES (%s, %s, %s, %s, %s)
            ''', (datos_inscripcion['nombre'], datos_inscripcion['apellido'], datos_inscripcion['usuario'], datos_inscripcion['contraseña'], datos_inscripcion['correo']))
            conn.commit()

# Cerrar la conexión a la base de datos al final del programa
cursor.close()
conn.close()