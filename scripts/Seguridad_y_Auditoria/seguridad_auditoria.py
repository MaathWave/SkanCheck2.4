#!/usr/bin/env python3

import os
import psutil
import time
import importlib.util
import subprocess
from datetime import datetime, timedelta
from prettytable import PrettyTable
#from watchdog.observers import Observer
#from watchdog.events import FileSystemEventHandler



# Verificar e instalar la biblioteca watchdog si es necesario

#def instalar_biblioteca_si_es_necesaria():
#    biblioteca = "watchdog"
#    try:
#        importlib.util.find_spec(biblioteca)
#    except ImportError:
#        print(f"La biblioteca {biblioteca} no está instalada. Instalando...")
#        subprocess.run(["pip", "install", biblioteca])

#instalar_biblioteca_si_es_necesaria()



def obtener_registros_de_seguridad():
    registros_seguridad = os.popen("cat /var/log/auth.log | tail -n 10").read().strip().split("\n")
    return registros_seguridad


#class CambiosEnArchivosHandler(FileSystemEventHandler):
#    def on_modified(self, event):
#        if not event.is_directory:
#            print(f"Archivo modificado: {event.src_path}")


#def monitorear_cambios_en_archivos(ruta):
#	event_handler = CambiosEnArchivosHandler()
#	observer = Observer()
#	observer.schedule(event_handler, path=ruta, recursive=False)
#	observer.start()
#	try:
#		while True:
#			time.sleep(1)
#	except KeyboardInterrupt:
#		observer.stop()
#	observer.join()



def monitorear_acceso_recursos_servicios():
    acceso_servicios = []
    for connection in psutil.net_connections(kind='inet'):
        acceso_servicios.append({
            "PID": connection.pid,
            "LADDR": connection.laddr,
            "RADDR": connection.raddr,
            "Estado": connection.status
        })
    return acceso_servicios



def main():
	print("Bienvenido a la herramienta de Seguridad y Auditoria\n")

	print("1. Registros de Seguridad (Últimos 10 registros):\n")
	registros_seguridad = obtener_registros_de_seguridad()
	for registro in registros_seguridad:
		print(registro)


	print("\n\n2. Monitorear Acceso a Recursos y Servicios:\n")
	print("Iniciando el monitoreo de acceso a recursos y servicios...\n")
	acceso_servicios = monitorear_acceso_recursos_servicios()
	tabla_acceso_servicios = PrettyTable()
	tabla_acceso_servicios.field_names = ["PID", "LADDR", "RADDR", "Estado"]
	for acceso in acceso_servicios:
		tabla_acceso_servicios.add_row([
			acceso["PID"],
			acceso["LADDR"],
			acceso["RADDR"],
			acceso["Estado"]
		])
	print(tabla_acceso_servicios)



#	print("\n\n3. Monitorear Cambios en Archivos Críticos:\n")
#	print(f"Iniciando el monitoreo de cambios en archivos criticos...\n")
#	print("Seleccione una de las opciones para escanear.")
#	print("1. Ultimas 72 horas\n2. Ultimas 48 horas\n3. Ultimas 24 horas\n4. En tiempo real")
#	opcion = input("\n ~ Seleccione una opcion: ")

#	if opcion == "1":
#		duracion = timedelta(hours=72)
#	elif opcion == "2":
#		duracion = timedelta(hours=48)
#	elif opcion == "3":
#		duracion = timedelta(hours=24)
#	elif opcion == "4":
#		ruta_archivos_criticos = '/etc'
#		print(f"Iniciando el monitoreo en cambios de archivos criticos en {ruta_archivos_criticos}...\n")
#		monitorear_cambios_en_archivos(ruta_archivos_criticos)
#		return
#	else:
#		print("Opcion no valida.")
#		return

#	fecha_inicio = datetime.now() - duracion
#	print(f"Iniciando el monitoreo de cambios en archivos criticos en las ultimas {duracion}... \n")
#	while True:
#		if datetime.now() >= fecha_inicio + duracion:
#			break
#		monitorear_cambios_en_archivos(ruta_archivos_criticos)



if __name__ == "__main__":
    main()

