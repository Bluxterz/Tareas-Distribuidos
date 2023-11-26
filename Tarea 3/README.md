# Ayudantia-Hadoop
joaquin.fernandez1@mail.udp.cl

Para levantar topologia de contenedores:
```sh
docker compose up --build
```
Para visualizar contenedores y sus estados:
```sh
docker ps -a
```
Para entrar a contenedores:
```sh
docker exec -it name_service_o_id bash
```
Para bajar arquitectura junto a los volumenes usar el siguiente comando:
```sh
docker compose down -v
```
Para borrar cache usar el siguiente comando luego de bajar todos los contenedores
```sh
docker system prune -a
```
Para borrar contenedores a mano sin la necesidad de usar el -v en el comando compose down:
```sh
docker volume rm $(docker volume ls -q)
```

---
## *Tutorial Hadoop*

Primero que todo ya deben de tener la topología levantada. Posterior de ello deben de visualizar los respectivo directorios con los cuales van a trabajar vendrían a ser examples y buscador. \
\
Otro detalle de suma relevancia, si es que están en windows, deben de cambiar el interprete de crlf a lf; puesto que si no lo hacen puede que les genere conflico para la lectura y ejecución de ciertos archivos al momento de realizar acciones de haddop como la sincronización de archivos sh y también archivos python en este caso que interactuan con la consola.\
\
**Los archivos que deben cambiar son mapper.py, reducer.py y docker-entrypoint.sh** 

Ahora  lo para trabajar con hadoop usaremos comandos basicos dentro de su repertorio y esto con el modivo de que es un manejador de archivos distribuido con nombre hdfs (Hadoop Distributed Files System). \
\
Posterior a lo anterior deben de configurar un usuario que administrará todos los comandos y por ello es necesario que sigan las siguientes instrucciones y/o comandos:

**[0]** Se accede al contenedor que contiene el servicio de hadoop:
```sh
docker exec -it hadoop bash
```
**[1]** Se creará un respectivo directorio para gestionar las acciones del usuario hduser (es imporatnte que tenga este nombre para todos los comandos)\
Creación de carpeta para usuario:
```sh
hdfs dfs -mkdir /user
```
Creación de usuario en el directorio:
```sh
hdfs dfs -mkdir /user/hduser
```
Creación de directorio para el procesamiento archivos y/o textos:
```sh
hdfs dfs -mkdir input
```
**[2]** Damos los permisos tantos del usuario y del directorio
```sh
sudo chown -R hduser .
```
**[3]** Cargamos los txt extraidos de wikipedia a hadoop mediante los siguientes comandos, primero accedemos a la carpeta donde estan alojados y se ejecuta hdfs.
```sh
cd examples/
hdfs dfs -put carpeta1/*.txt input
hdfs dfs -put carpeta2/*.txt input
```
Se puede validar que efectivamente se hayan procesado dichos archivos contenidos en los directorios con el siguiente comando:
```sh
hdfs dfs -ls input
```
Con eso ya deberían de tener un seguimiento de los arhicovs traspasados al directorio input dentro administrador de archivos de Hadoop.

**[4]** Se ejecutan tanto mapper y reducer puesto que hadoop trabaja con ambas.
```sh
mapred streaming -files mapper.py,reducer.py -input /user/hduser/input/*.txt -output hduser/outhadoop/ -mapper ./mapper.py -reducer ./reducer.py
```
Luego el archivo lo exportamos al entorno local en linux dentro del contenedor y en este caso dentro del directorio examples. Allí quedará una carpeta de nombre output con un contador de palabras por archivo y en este caso sería uno general para todos los datos volcados tanto en la *carpeta1* como en la *carpeta2*. 

Es aquí donde entra el uso del volumen para así extraer de forma efectiva el archivo ya procesado, por hadoop.
```sh
hdfs dfs -get /user/hduser/hduser/outhadoop/ /home/hduser/examples
```

Con lo anterior ya estarían listos con la respectiva aplicación (revisen la carpeta outputdoop y fijense en el archivo part-00000). \
Allí verán que saldrá una columna que representa el número de documento y también otra que representa la frecuencia o la cantidad de veces que pueden encontrar dicha palabra en el .txt procesado, cabe recalcar que es un archivo que volcará todas las palabras de los 10 archivos contenidos en ambas carpetas.
