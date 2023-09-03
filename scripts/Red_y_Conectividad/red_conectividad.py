#!/usr/bin/env python3

import os
import netifaces
import subprocess
from prettytable import PrettyTable


def obtener_informacion_red():
    interfaces = netifaces.interfaces()

    informacion_interfaces = []
    for iface in interfaces:
        iface_info = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in iface_info:
            ipv4_info = iface_info[netifaces.AF_INET][0]
            ip = ipv4_info['addr']
            mascara = ipv4_info['netmask']
            mac = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']
            informacion_interfaces.append({
                "Interfaz": iface,
                "IP": ip,
                "Máscara": mascara,
                "MAC": mac
            })

    return informacion_interfaces

def obtener_puertos_abiertos():
    output = os.popen("netstat -tuln").read()
    lineas = output.split("\n")
    puertos_abiertos = []

    for linea in lineas[2:]:
        partes = linea.split()
        if len(partes) >= 4:
            puerto = partes[3].split(":")[-1]
            puertos_abiertos.append(puerto)

    return puertos_abiertos

def obtener_informacion_enrutamiento():
    output = os.popen("ip route").read().strip()
    informacion_enrutamiento = output.splitlines()
    return informacion_enrutamiento

def obtener_estado_conexion(host):
    result = subprocess.run(["ping", "-c", "4", host], capture_output=True, text=True)
    return result.stdout

def main():
    print("Información de Interfaces de Red:\n")
    tabla_interfaces = PrettyTable()
    tabla_interfaces.field_names = ["Interfaz", "IP", "Máscara", "MAC"]
    informacion_interfaces = obtener_informacion_red()
    for iface_info in informacion_interfaces:
        tabla_interfaces.add_row([
            iface_info["Interfaz"],
            iface_info["IP"],
            iface_info["Máscara"],
            iface_info["MAC"]
        ])
    print(tabla_interfaces)

    print("\nPuertos Abiertos:\n")
    puertos_abiertos = obtener_puertos_abiertos()
    print(", ".join(puertos_abiertos))

    print("\nInformación de Enrutamiento:\n")
    informacion_enrutamiento = obtener_informacion_enrutamiento()
    tabla_enrutamiento = PrettyTable()
    tabla_enrutamiento.field_names = ["Destino", "Máscara", "Gateway", "Interfaz"]
    for linea in informacion_enrutamiento:
        partes = linea.split()
        destino = partes[0]
        mascara = partes[1]
        gateway = partes[2]
        interfaz = partes[4]
        tabla_enrutamiento.add_row([destino, mascara, gateway, interfaz])
    print(tabla_enrutamiento)

    print("\nEstado de Conexión:\n")
    hosts_a_ping = ["8.8.8.8", "192.168.1.1", "www.google.com"]
    for host in hosts_a_ping:
        print("=" * 40)
        print(f"Estado de conexión a {host}:\n")
        estado_conexion = obtener_estado_conexion(host)

        if "4 received" in estado_conexion:
            print("Conexión exitosa: Todos los paquetes recibidos.")
        elif "0 received" in estado_conexion:
            print("Pérdida de paquetes: Ningún paquete recibido.")
        else:
            print("Algunos paquetes perdidos: Ver detalles a continuación.")

        print(estado_conexion)
        print("\n")


if __name__ == "__main__":
    main()

