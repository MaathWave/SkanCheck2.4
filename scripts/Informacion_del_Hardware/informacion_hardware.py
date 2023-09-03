#!/usr/bin/env python3

import platform
import subprocess
import pyudev
from prettytable import PrettyTable


def instalar_lshw():
	try:
		print("Instalando el paquete lshw...")
		subprocess.run(["sudo", "apt-get", "install", "lshw", "-y"], check=True)
		print(" --- lshw se ha instalado correctamente. ---")
	except subprocess.CalledProcessError:
		print("No se pudo instalar lshw. Asegúrate de tener privilegios de superusuario.")



def obtener_informacion_sistema():
    informacion_sistema = {
        "Sistema Operativo": platform.system(),
        "Versión del Sistema Operativo": platform.release(),
        "Arquitectura": platform.architecture(),
        "Hostname": platform.node(),
        "Procesador": platform.processor()
    }
    return informacion_sistema

def obtener_especificaciones_hardware():
    try:
        salida = subprocess.check_output(["lshw", "-short", "-class", "system,processor,memory,storage"])
        especificaciones_hardware = salida.decode("utf-8").strip().split("\n")
        return especificaciones_hardware
    except subprocess.CalledProcessError:
        return ["No se pudo obtener información de hardware"]

def obtener_dispositivos_conectados():
    dispositivos_conectados = []
    context = pyudev.Context()
    for device in context.list_devices(subsystem='usb'):
        dispositivos_conectados.append({
            "Dispositivo": device.get('ID_MODEL', 'Desconocido'),
            "ID del Producto": device.get('ID_MODEL_ID', 'Desconocido'),
            "Fabricante": device.get('ID_VENDOR', 'Desconocido')
        })
    return dispositivos_conectados


def main():
    instalar_lshw()

    print("\nInformación del Sistema:\n")
    informacion_sistema = obtener_informacion_sistema()
    tabla_informacion_sistema = PrettyTable()
    tabla_informacion_sistema.field_names = ["Categoría", "Valor"]
    for categoria, valor in informacion_sistema.items():
        tabla_informacion_sistema.add_row([categoria, valor])
    print(tabla_informacion_sistema)

    print("\nEspecificaciones de Hardware:\n")
    especificaciones_hardware = obtener_especificaciones_hardware()
    for linea in especificaciones_hardware:
        print(linea)

    print("\nDispositivos Conectados:\n")
    dispositivos_conectados = obtener_dispositivos_conectados()
    tabla_dispositivos_conectados = PrettyTable()
    tabla_dispositivos_conectados.field_names = ["Dispositivo", "ID del Producto", "Fabricante"]
    for dispositivo in dispositivos_conectados:
        tabla_dispositivos_conectados.add_row([
            dispositivo["Dispositivo"],
            dispositivo["ID del Producto"],
            dispositivo["Fabricante"]
        ])
    print(tabla_dispositivos_conectados)



if __name__ == "__main__":
    main()

