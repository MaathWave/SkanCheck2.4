#!/usr/bin/env python3

import os
import psutil
import socket
from prettytable import PrettyTable

def obtener_informacion_configuracion_red():
    interfaces = psutil.net_if_addrs()

    informacion_interfaces = []
    for iface, addrs in interfaces.items():
        iface_info = {
            "Interfaz": iface,
            "Dirección IP": "",
            "Máscara de Subred": "",
            "MAC": ""
        }
        for addr in addrs:
            if addr.family == socket.AF_INET:
                iface_info["Dirección IP"] = addr.address
                iface_info["Máscara de Subred"] = addr.netmask
            elif addr.family == psutil.AF_LINK:
                iface_info["MAC"] = addr.address
        informacion_interfaces.append(iface_info)

    return informacion_interfaces


def obtener_ajustes_firewall():
	ajustes_firewall = os.popen("sudo iptables -L").read().strip().split("\n")[2:]
	return ajustes_firewall


def obtener_politicas_seguridad():
    politicas_seguridad = os.popen("sudo apparmor_status").read().strip().split("\n")
    return politicas_seguridad


def obtener_configuracion_enrutamiento_enlace():
    configuracion_enrutamiento = os.popen("ip route").read().strip().split("\n")
    configuracion_enlace = os.popen("ip link show").read().strip().split("\n")
    return configuracion_enrutamiento, configuracion_enlace


def main():
	print("Información de Configuración de Red:\n")
	informacion_configuracion_red = obtener_informacion_configuracion_red()
	tabla_configuracion_red = PrettyTable()
	tabla_configuracion_red.field_names = ["Interfaz", "Dirección IP", "Máscara de Subred", "MAC"]
	for iface_info in informacion_configuracion_red:
		tabla_configuracion_red.add_row([
			iface_info["Interfaz"],
			iface_info["Dirección IP"],
			iface_info["Máscara de Subred"],
			iface_info["MAC"]
			])
		print(tabla_configuracion_red)


	print("\nAjustes de Firewall:\n")
	ajustes_firewall = obtener_ajustes_firewall()
	tabla_ajustes_firewall = PrettyTable()
	tabla_ajustes_firewall.field_names = ["Número de Regla", "Acción", "Protocolo", "Origen", "Destino", ""]
	for linea in ajustes_firewall:
		partes = linea.split()
		if partes and partes[0].isdigit() and len(partes) >= 5:
			tabla_ajustes_firewall.add_row(partes[1:5])
	print(tabla_ajustes_firewall)


	print("\nPolíticas de Seguridad:\n")
	politicas_seguridad = obtener_politicas_seguridad()
	tabla_politicas_seguridad = PrettyTable()
	for linea in politicas_seguridad:
		tabla_politicas_seguridad.add_row([linea])
	print(tabla_politicas_seguridad)


	print("\nConfiguración de Enrutamiento y Enlace:\n")
	configuracion_enrutamiento, configuracion_enlace = obtener_configuracion_enrutamiento_enlace()

	print("Configuración de Enrutamiento:")
	tabla_enrutamiento = PrettyTable()
	tabla_enrutamiento.field_names = ["Destino", "Via" , "Interfaz", "Protocolo", "Origen", "Metrica"]
	for linea in configuracion_enrutamiento:
		partes = linea.split()
		if len(partes) >= 11:
			destino = partes[0]
			via = partes[2] if partes[1] == "via" else ""
			interfaz = partes[4] if partes[3] == "dev" else ""
			protocolo = partes[6] if partes[5] == "proto" else ""
			origen = partes[8] if partes[7] == "src" else ""
			metrica = partes[10] if partes[9] == "metric" else ""
			tabla_enrutamiento.add_row([destino, via, interfaz, protocolo, origen, metrica])
	print(tabla_enrutamiento)


	print("\nConfiguración de Enlace:\n")
	tabla_enlace = PrettyTable()
	tabla_enlace.field_names = ["Interfaz", "MAC", "Estado"]
	for linea in configuracion_enlace:
		partes = linea.split()
		if partes[1] != "lo:":
			tabla_enlace.add_row(partes[:3])
	print(tabla_enlace)



if __name__ == "__main__":
    main()


