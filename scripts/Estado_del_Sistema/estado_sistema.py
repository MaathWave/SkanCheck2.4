#!/usr/bin/env python3

import os
import psutil
from prettytable import PrettyTable


def obtener_descripcion_carga(carga_promedio):
    if carga_promedio < 1:
        return "Baja"
    elif carga_promedio < 2:
        return "Moderada"
    else:
        return "Alta"

def formatear_bytes(bytes_valor):
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_valor < 1024.0:
            return f"{bytes_valor:.2f} {unidad}"
        bytes_valor /= 1024.0

def formatear_porcentaje(porcentaje):
    return f"{porcentaje:.2f}%"


def estado_del_sistema():
    carga_sistema = os.getloadavg()
    carga_promedio_1min = carga_sistema[0]
    carga_promedio_5min = carga_sistema[1]
    carga_promedio_15min = carga_sistema[2]

    memoria = psutil.virtual_memory()
    mem_total = formatear_bytes(memoria.total)
    mem_disponible = formatear_bytes(memoria.available)
    mem_utilizada = formatear_bytes(memoria.used)
    mem_porcentaje = formatear_porcentaje(memoria.percent)

    info_cpu = {
        "Núcleos": psutil.cpu_count(logical=False),
        "Hilos": psutil.cpu_count(logical=True),
        "Frecuencia": f"{psutil.cpu_freq().current} MHz",
        "Modelo": os.popen("cat /proc/cpuinfo | grep 'model name' | uniq").read().strip().split(":")[1]
    }

    carga_nucleos = psutil.cpu_percent(interval=0.1, percpu=True)

    info_cpu["Carga de Nucleos (%)"] = ", ".join([f"Nucleo {i}: {carga:.2f}" for i, carga in enumerate(carga_nucleos)])
    info_cpu["Arquitectura"] = os.popen("lscpu | grep 'Architecture' | awk '{print $2}'").read().strip()
    info_cpu["Tipo de CPU"] = os.popen("lscpu | grep 'Model name' | awk '{$1=\"\"; $2=\"\"; $3=\"\"; print $0}'").read().strip()

    almacenamiento = os.statvfs("/")
    almacenamiento_total = almacenamiento.f_frsize * almacenamiento.f_blocks
    almacenamiento_disponible = almacenamiento.f_frsize * almacenamiento.f_bavail
    almacenamiento_utilizado = almacenamiento_total - almacenamiento_disponible

    almacenamiento_total_formatted = formatear_bytes(almacenamiento_total)
    almacenamiento_disponible_formatted = formatear_bytes(almacenamiento_disponible)
    almacenamiento_utilizado_formatted = formatear_bytes(almacenamiento_utilizado)

    estado_sistema = {
        "Carga del Sistema": carga_sistema,
        "Memoria": {
            "Total": mem_total,
            "Disponible": mem_disponible,
            "Utilizada": mem_utilizada,
            "Porcentaje Utilizado": mem_porcentaje
        },
        "CPU": info_cpu,
        "Almacenamiento": {
            "Total": almacenamiento_total_formatted,
            "Disponible": almacenamiento_disponible_formatted,
            "Utilizado": almacenamiento_utilizado_formatted
        }
    }

    return estado_sistema


def main():
    estado_sistema = estado_del_sistema()

    for categoria, info in estado_sistema.items():
        print(f"{categoria}:\n")
        if categoria == "Carga del Sistema":
            tabla_carga = PrettyTable()
            tabla_carga.field_names = ["Período", "Carga Promedio", "Descripción"]
            tabla_carga.add_row(["1 min", estado_sistema["Carga del Sistema"][0], obtener_descripcion_carga(estado_sistema["Carga del Sistema"][0])])
            tabla_carga.add_row(["5 min", estado_sistema["Carga del Sistema"][1], obtener_descripcion_carga(estado_sistema["Carga del Sistema"][1])])
            tabla_carga.add_row(["15 min", estado_sistema["Carga del Sistema"][2], obtener_descripcion_carga(estado_sistema["Carga del Sistema"][2])])
            print(tabla_carga)
        elif isinstance(info, dict):
            tabla = PrettyTable()
            tabla.field_names = ["Métrica", "Valor"]
            for sub_categoria, valor in info.items():
                tabla.add_row([sub_categoria, valor])
            print(tabla)
        else:
            print(info)
        print("\n")



if __name__ == "__main__":
    main()

