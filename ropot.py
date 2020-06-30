#######.  #!/usr/bin/env python


from shutil import copyfile

from datetime import datetime

from numpy import genfromtxt

from matplotlib.dates import DateFormatter

import subprocess

import re

import numpy as np

import matplotlib

import matplotlib.dates as mdates

import pandas as pd

import sys
sys.path.append('/home/pi/snappy-sms-movistar')
from snappy_sms import send_sms

from paramiko import SSHClient

from paramiko import AutoAddPolicy
from scp import SCPClient


######sudo pip install python-pushover
from pushover import Client
print "Conectando con el Ropot ..."

# ff Hagamos algo chulo

matplotlib.use('Agg')

import matplotlib.pyplot as plt


# ff vamos a leer el sensor

miFloraResult = None

tries = 0

while miFloraResult is None:

    if tries > 10:

        sys.exit("10 intentos mas?")

    try:
        ###### CAMBIAR AQUI LA MAC

        miFlora = subprocess.Popen('/home/pi/miflora/miflora AC:DC:AC:DC:AC:DC hci0', shell=True, stdout=subprocess.PIPE)

        result = miFlora.stdout.read()

        if "Error" not in result:

                miFloraResult = result

                print "Lectura de Xiaomi Ropot"

        else:

                print "Error al leer Xiaomi Ropot"

    except:

         pass

    tries = tries + 1


# ff Ahora buscamos en el resultado

miTemp = float(re.search(r"Temperature:(\d*[.\d]*)", miFloraResult).group(1))

miMoist = int(re.search(r"Moisture:(\d*)", miFloraResult).group(1))

miConductivity = int(re.search(r"Conductivity:(\d*)", miFloraResult).group(1))

miLight = int(re.search(r"Light:(\d*)", miFloraResult).group(1))

miBattery = int(re.search(r"Battery:(\d*)", miFloraResult).group(1))

###2020 le metemos esto para evitar que si falla la lectura nos escriba valores cero

if miTemp + miMoist + miConductivity == 0:
        sys.exit()
##############Fin de la chorrada de 2020#############################################3



# ff decidimos que imagenes vamos a usar

if miTemp < 18:

        temp = 'temp1.jpg'

elif miTemp <= 25:

        temp = 'temp2.jpg'

elif miTemp > 25:

        temp = 'temp3.jpg'


if miMoist < 20:

        moist = 'moist1.jpg'

elif miMoist <= 60:

        moist = 'moist2.jpg'

elif miMoist > 60:

        moist = 'moist3.jpg'


if miConductivity < 300:

        condu = 'condu1.jpg'

elif miConductivity <= 1200:

        condu = 'condu2.jpg'

elif miConductivity > 1200:

        condu = 'condu3.jpg'


if miLight < 25:

        luz = 'luz1.jpg'

elif miLight <= 500:

        luz = 'luz2.jpg'

elif miLight > 500:

        luz = 'luz3.jpg'


# ff guardamos los datos en un ficherillo de texto

#### CAMBIAR AQUI LOS NOMBRES DE LOS FICHEROS DE BBDD

dt = datetime.now().strftime('%Y-%m-%d %H:%M')


text_file = open("humedad_ropot.txt", "a")

text_file.write (dt +","+ str(miMoist) + "\n")

text_file.close()


text_file = open("nutrientes_ropot.txt", "a")

text_file.write (dt +","+ str(miConductivity) + "\n")

text_file.close()


text_file = open("temp_ropot.txt", "a")

text_file.write (dt +","+ str(miTemp) + "\n")

text_file.close()


text_file = open("luz_ropot.txt", "a")

text_file.write (dt +","+ str(miLight) + "\n")

text_file.close()


# ff es bueno hacer un poco de orden en la base de datos

maxLines = 1000


with open('nutrientes_ropot.txt', 'r') as fcount:

        removeLines = sum(1 for line in fcount) - maxLines

if removeLines > 0:

        data="".join(open("nutrientes_ropot.txt").readlines()[removeLines:])

        open("nutrientes_ropot.txt","wb").write(data)


with open('luz_ropot.txt', 'r') as fcount:

        removeLines = sum(1 for line in fcount) - maxLines

if removeLines > 0:

        data="".join(open("luz_ropot.txt").readlines()[removeLines:])

        open("luz_ropot.txt","wb").write(data)


with open('temp_ropot.txt', 'r') as fcount:

        removeLines = sum(1 for line in fcount) - maxLines

if removeLines > 0:

        data="".join(open("temp_ropot.txt").readlines()[removeLines:])

        open("temp_ropot.txt","wb").write(data)


with open('humedad_ropot.txt', 'r') as fcount:

        removeLines = sum(1 for line in fcount) - maxLines

if removeLines > 0:

        data="".join(open("humedad_ropot.txt").readlines()[removeLines:])

        open("humedad_ropot.txt","wb").write(data)


# ff hacemos unos grafiquillos

        # luz

headers = ['Date','Lux']

df = pd.read_csv('luz_ropot.txt',names=headers)

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S.%f')

df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))

x = df['Date']

y = df['Lux']

plt.ylabel('Lux')

plt.plot(x,y)

formatter = DateFormatter('%d-%m %H:%M')

plt.gcf().axes[0].xaxis.set_major_formatter(formatter)

plt.title('Intensidad de la luz')

plt.gcf().autofmt_xdate()

plt.savefig("/home/pi/miflora/web/plotlicht_ropot.png")


        # temp

plt.clf()

headers = ['Date','Temp']

df = pd.read_csv('temp_ropot.txt',names=headers)

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S.%f')

df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))

x = df['Date']

y = df['Temp']

plt.ylabel('Grados')

plt.plot(x,y)

formatter = DateFormatter('%d-%m %H:%M')

plt.gcf().axes[0].xaxis.set_major_formatter(formatter)

plt.title('Temperatura')

plt.gcf().autofmt_xdate()

plt.savefig("/home/pi/miflora/web/plottemp_ropot.png")


        # nutrientes

plt.clf()

headers = ['Date','Conductivity']

df = pd.read_csv('nutrientes_ropot.txt',names=headers)

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S.%f')

df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))

x = df['Date']

y = df['Conductivity']

plt.ylabel('microSiemens/cm')

plt.plot(x,y)

formatter = DateFormatter('%d-%m %H:%M')

plt.gcf().axes[0].xaxis.set_major_formatter(formatter)

plt.title('Abono')

plt.gcf().autofmt_xdate()

plt.savefig("/home/pi/miflora/web/plotnutrientes_ropot.png")


        # humedad

plt.clf()

headers = ['Date','Moist']

df = pd.read_csv('humedad_ropot.txt',names=headers)

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S.%f')

df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))

x = df['Date']

y = df['Moist']

plt.ylabel('humedad porcentaje')

plt.plot(x,y)

formatter = DateFormatter('%d-%m %H:%M')

plt.gcf().axes[0].xaxis.set_major_formatter(formatter)

plt.title('Humedad')

plt.gcf().autofmt_xdate()

plt.savefig("/home/pi/miflora/web/plothumedad_ropot.png")


# ff Y hacemos el html resultante
## Le anadimos los datos de los rangos optimos que nos pasa la app de miflora para la planta

text_file = open("/home/pi/miflora/web/index.html", "w")

text_file.write("<html>")

text_file.write("<head>")

text_file.write("<title>Estadisticas del Ropot</title>")

text_file.write("<meta http-equiv=\"refresh\" content=\"10\">")

text_file.write("</head>")

text_file.write("<body>")

text_file.write("<basefont face='Verdana' size='2'")

text_file.write("<p><h1>Ropot</h1></p>")

text_file.write("<p><img src='images/"+ moist +"' height='100' width='100'>  <img src='images/"+ condu +"' height='100' width='120'> <img src='images/"+ temp +"' height='100' width='90'> <img src='images/"+ luz +"' height='100' width='100'></p>")

text_file.write("<p><h2>Datos Ropot</font></h2></p>")

text_file.write("Temperatura: " +  str(miTemp) + " grados")

text_file.write("</br>Humedad: " + str(miMoist) + "% Optimo (20-60)")

text_file.write("</br>Abono: " +  str(miConductivity) + " microSiemens/cm Optimo (350 2.000)")

text_file.write("</br>Luminosidad: " +  str(miLight) + " lux")

text_file.write("</br>Bateria: " +  str(miBattery) + "%")

text_file.write("</br></br>Ultima actualizacion: " + datetime.now().strftime('%d %B %H:%M:%S'))

text_file.write("<p><b><h2>Historico</h2></b></p>")

text_file.write("</br><img src='plothumedad_ropot.png'>")

text_file.write("</br><img src='plotnutrientes_ropot.png'>")

text_file.write("</br><img src='plottemp_ropot.png'>")

text_file.write("</br><img src='plotlicht_ropot.png'>")

text_file.write("</font></body>")

text_file.write("</html>")

text_file.close()


text_file = open("bateria_actual_ropot.txt", "w")
text_file.write(str(miBattery))
text_file.close()



##ff Y ahora nos montamos los ficheros para rrdtool

text_file = open("ropot_bateria.txt", "w")
text_file.write(str(miBattery))
text_file.close()

text_file = open("ropot_humedad.txt", "w")
text_file.write ( str(miMoist))
text_file.close()


text_file = open("ropot_nutrientes.txt", "w")
text_file.write ( str(miConductivity) )
text_file.close()


text_file = open("ropot_temp.txt", "w")
text_file.write ( str(miTemp) )
text_file.close()


text_file = open("ropot_luz.txt", "w")
text_file.write ( str(miLight))
text_file.close()


## Y le hacemos un ssh a comet para subirlos y usarlos en linknx



ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect("192.168.1.XXX",username="pi",password="passwordmegadificildeadivinar")

#SCP connectin
scp = SCPClient(ssh.get_transport(), sanitize=lambda x: x)
scp.put("ropot_bateria.txt", "/var/lib/linknx/")
scp.put("ropot_humedad.txt", "/var/lib/linknx/")
scp.put("ropot_nutrientes.txt", "/var/lib/linknx/")
scp.put("ropot_temp.txt", "/var/lib/linknx/")
scp.put("ropot_luz.txt", "/var/lib/linknx/")

scp.close()

ssh.close()





###ff Y hacemos el miniframe

text_file = open("/home/pi/miflora/web/ropot_frame.html", "w")

text_file.write("<html>")

text_file.write("<head>")

text_file.write("<title>Estadisticas de la Ropot</title>")

text_file.write("<meta http-equiv=\"refresh\" content=\"10\">")

text_file.write("</head>")

text_file.write("<body>")

text_file.write("<basefont face='Verdana' size='2'")

text_file.write("<p><h2>Datos Ropot</font></h2></p>")

text_file.write("Temperatura: " +  str(miTemp) + " grados")

text_file.write("</br>Humedad: " + str(miMoist) + "%")

text_file.write("</br>Abono: " +  str(miConductivity) + " micro S/cm")

text_file.write("</br>Luminosidad: " +  str(miLight) + " lux")

text_file.write("</br>Bateria: " +  str(miBattery) + "%")

text_file.write("</br>Actualizacion: " + datetime.now().strftime('%d %B %H:%M:%S'))

text_file.write("</font></body>")

text_file.write("</html>")

text_file.close()



##ff Y hacemos el last update

text_file = open("/home/pi/miflora/web/ropot_last_update.html", "w")

text_file.write("<html>")

text_file.write("<head>")

#text_file.write("<title>Last updated Hortensia Norte</title>")

#text_file.write("<meta http-equiv=\"refresh\" content=\"10\">")

text_file.write("</head>")

text_file.write("<body>")

text_file.write("<basefont face='Verdana' size='2'")

#text_file.write("</br>Ultima actualizacion: " + datetime.now().strftime('%d %B %H:%M:%S'))

text_file.write("</br>" + datetime.now().strftime('%d %B %H:%M:%S'))

text_file.write("</font></body>")

text_file.write("</html>")

text_file.close()


















#######Y le meyemos notificaciones por pushover  y por SMS
####### Si la humedad se va de parametros
### Por SMS ya no porque los de Movistar son unos cutres y te cobran a 20 cts el SMS

#if miMoist < 20:
#    client = Client("pushoverclient", api_token="tokeldelpushover")
#    client.send_message(str(miMoist), title="Humedad Planta")
###    send_sms(610687843, 'La humedad de la Planta es ' + str(miMoist))

#elif miMoist >= 60:
#    client = Client("pushoverclient", api_token="tokeldelpushover")
#    client.send_message(str(miMoist), title="Humedad Planta")
###    send_sms(666666666, 'La humedad de la Planta es ' + str(miMoist))

if miBattery <= 20:
    client = Client("pushoverclient", api_token="tokeldelpushover")
    client.send_message(str(miBattery), title="Bateria Ropot Baja")
