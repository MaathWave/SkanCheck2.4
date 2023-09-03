#!/usr/bin/env python3

import os
import subprocess
import apt
import pkg_resources
from prettytable import PrettyTable


def obtener_paquetes_instalados():
	cache = apt.Cache()
	paquetes_instalados = [pkg.name for pkg in cache if pkg.is_installed]
	return paquetes_instalados


def obtener_actualizaciones_pendientes():
    cache = apt.Cache()
    paquetes_actualizables = [pkg.name for pkg in cache if pkg.is_upgradable]
    return paquetes_actualizables


def obtener_versiones_software():
    versiones_software = []
    for package in pkg_resources.working_set:
        versiones_software.append({
            "Paquete": package.project_name,
            "Versión": package.version
        })
    return versiones_software


def main():
	print("Paquetes Instalados:\n")
	paquetes_instalados = obtener_paquetes_instalados()
	tabla_paquetes_instalados = PrettyTable()
	tabla_paquetes_instalados.field_names = ["Indice", "Nombre"]
	for i, nombre_paquete in enumerate(paquetes_instalados, start=1):
		tabla_paquetes_instalados.add_row([i, nombre_paquete])
	print(tabla_paquetes_instalados)


	print("\nActualizaciones Pendientes:\n")
	paquetes_actualizables = obtener_actualizaciones_pendientes()
	tabla_paquetes_actualizables = PrettyTable()
	tabla_paquetes_actualizables.field_names = ["Paquete"]
	tabla_paquetes_actualizables.add_column("Nombre", paquetes_actualizables)
	print(tabla_paquetes_actualizables)


	print("\nVersiones de Software:\n")
	versiones_software = obtener_versiones_software()
	tabla_versiones_software = PrettyTable()
	tabla_versiones_software.field_names = ["Paquete", "Versión"]
	for version in versiones_software:
		tabla_versiones_software.add_row([
			version["Paquete"],
			version["Versión"]
		])
	print(tabla_versiones_software)



if __name__ == "__main__":
    main()

