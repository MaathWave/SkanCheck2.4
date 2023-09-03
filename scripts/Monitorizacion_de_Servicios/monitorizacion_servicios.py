#!/usr/bin/env python3

import os
import requests
import subprocess
from prettytable import PrettyTable



def verificar_estado_servicio(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return "Activo"
        else:
            return "Inactivo"
    except requests.exceptions.RequestException:
        return "Inactivo"

def obtener_registros_aplicaciones(aplicacion):
    registros = os.popen(f"tail -n 10 /var/log/{aplicacion}.log").read().strip().split("\n")
    return registros

def obtener_metricas_aplicaciones(aplicacion):
    metricas = subprocess.getoutput(f"cat /var/metrics/{aplicacion}.metrics")
    return metricas

def main():
    servicios_criticos = {
        "HTTP": "http://localhost",
        "Base de Datos": "http://localhost:3306",
        "Correo Electrónico": "http://localhost:25"
    }

    print("\nEstado de Servicios Críticos:\n")
    tabla_estado_servicios = PrettyTable()
    tabla_estado_servicios.field_names = ["Servicio", "Estado"]
    for servicio, url in servicios_criticos.items():
        estado = verificar_estado_servicio(url)
        tabla_estado_servicios.add_row([servicio, estado])
    print(tabla_estado_servicios)

    print("\nRegistros de Aplicaciones:\n")
    aplicaciones_monitorizadas = ["app1", "app2"]
    for aplicacion in aplicaciones_monitorizadas:
        estado_servicio = verificar_estado_servicio(aplicacion)
        if estado_servicio == "Activo":
            registros = obtener_registros_aplicaciones(aplicacion)
            print(f"Registros de {aplicacion}:\n")
            if registros:
                for registro in registros:
                    print(registro)
            else:
                print(f"No hay registros disponibles para {aplicacion} en este momento.")
        else:
            print(f"El servicio de {aplicacion} está inactivo.")

    print("\n\nMétricas de Aplicaciones:\n")
    for aplicacion in aplicaciones_monitorizadas:
        estado_servicio = verificar_estado_servicio(aplicacion)
        if estado_servicio == "Activo":
            metricas = obtener_metricas_aplicaciones(aplicacion)
            print(f"Métricas de {aplicacion}:\n")
            print(metricas)
        else:
            print(f"No hay métricas disponibles para {aplicacion} en este momento.")



if __name__ == "__main__":
    main()

