#!/usr/bin/env python3

import os
import psutil
import requests
import subprocess
import time
from prettytable import PrettyTable


def instalar_iftop_si_es_necesario():
    try:
        subprocess.run(["iftop", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except:
        print("El comando iftop no esta instalado. Instalando...")
        subprocess.run(["sudo", "apt-get", "install", "iftop"])

instalar_iftop_si_es_necesario()



def obtener_rendimiento_cpu():
    rendimiento_cpu = psutil.cpu_percent(interval=1, percpu=True)
    return rendimiento_cpu


def obtener_rendimiento_memoria():
    rendimiento_memoria = psutil.virtual_memory()
    return rendimiento_memoria


def obtener_rendimiento_entrada_salida():
    rendimiento_entrada_salida = psutil.disk_io_counters()
    return rendimiento_entrada_salida


def obtener_tiempo_respuesta_aplicacion(url, tiempo_max_espera=5):
	try:
		response = requests.get(url, timeout=tiempo_max_espera)
		tiempo_respuesta = response.elapsed.total_seconds() * 1000
		return tiempo_respuesta
	except requests.exceptions.Timeout:
		return "N/A"
	except requests.exceptions.RequestException:
		return "N/A"


def obtener_analisis_carga_red(tiempo_maximo=60):
	carga_red = []
	comando_iftop = ["sudo", "iftop"]
	proceso_iftop = subprocess.Popen(comando_iftop, stdout=subprocess.PIPE)

	try:
		tiempo_inicio = time.time()
		while time.time() - tiempo_inicio < tiempo_maximo:
			linea = proceso_iftop.stdout.readline().decode("utf-8").strip()
			if not linea:
				break
			carga_red.append(linea)
	except KeyboardInterrupt:
		pass
	finally:
		proceso_iftop.terminate()

	return carga_red



def main():
	print("\nRendimiento del CPU:\n")
	rendimiento_cpu = obtener_rendimiento_cpu()
	tabla_rendimiento_cpu = PrettyTable()
	tabla_rendimiento_cpu.field_names = ["Núcleo", "Uso (%)"]
	for i, uso in enumerate(rendimiento_cpu):
		tabla_rendimiento_cpu.add_row([f"Núcleo {i}", f"{uso:.2f}%"])
	print(tabla_rendimiento_cpu)

	print("\nRendimiento de la Memoria:\n")
	rendimiento_memoria = obtener_rendimiento_memoria()
	tabla_rendimiento_memoria = PrettyTable()
	tabla_rendimiento_memoria.field_names = ["Métrica", "Valor"]
	tabla_rendimiento_memoria.add_row(["Total", f"{rendimiento_memoria.total / (1024 ** 3):.2f} GB"])
	tabla_rendimiento_memoria.add_row(["Disponible", f"{rendimiento_memoria.available / (1024 ** 3):.2f} GB"])
	tabla_rendimiento_memoria.add_row(["Utilizada", f"{rendimiento_memoria.used / (1024 ** 3):.2f} GB"])
	tabla_rendimiento_memoria.add_row(["Porcentaje Utilizado", f"{rendimiento_memoria.percent:.2f}%"])
	print(tabla_rendimiento_memoria)

	print("\nRendimiento de Entrada/Salida:\n")
	rendimiento_entrada_salida = obtener_rendimiento_entrada_salida()
	tabla_rendimiento_entrada_salida = PrettyTable()
	tabla_rendimiento_entrada_salida.field_names = ["Métrica", "Valor"]
	tabla_rendimiento_entrada_salida.add_row(["Lecturas", f"{rendimiento_entrada_salida.read_bytes / (1024 ** 3):.2f} GB"])
	tabla_rendimiento_entrada_salida.add_row(["Escrituras", f"{rendimiento_entrada_salida.write_bytes / (1024 ** 3):.2f} GB"])
	print(tabla_rendimiento_entrada_salida)

	print("\nTiempo de Respuesta de Aplicaciones:\n")
	aplicaciones_a_monitorear = {
		"Aplicación 1": "https://httpbin.org/delay/1",
		"Aplicación 2": "https://www.google.com",
		"Aplicacion 3": "https://www.youtube.com",
		"Aplicacion 4": "https://www.campusciberseguridad.com/"
	}
	tabla_tiempo_respuesta = PrettyTable()
	tabla_tiempo_respuesta.field_names = ["Aplicación", "Tiempo de Respuesta (ms)"]
	for aplicacion, url in aplicaciones_a_monitorear.items():
		tiempo_respuesta = obtener_tiempo_respuesta_aplicacion(url)
		if tiempo_respuesta == "N/A":
			tiempo_respuesta_str = tiempo_respuesta
		else:
			tiempo_respuesta_str = f"{tiempo_respuesta:.2f} ms"
		tabla_tiempo_respuesta.add_row([aplicacion, tiempo_respuesta_str])
	print(tabla_tiempo_respuesta)

#	print("\nAnálisis de Carga de Red:\n")
#	tiempo_maximo_analisis = 60
#	analisis_carga_red = obtener_analisis_carga_red(tiempo_maximo=tiempo_maximo_analisis)
#
#	for linea in analisis_carga_red:
#		print(linea)



if __name__ == "__main__":
    main()

