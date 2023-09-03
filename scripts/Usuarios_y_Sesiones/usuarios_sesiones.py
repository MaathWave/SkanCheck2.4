#!/usr/bin/env python3

import os
import psutil
from prettytable import PrettyTable

def obtener_usuarios_activos():
    usuarios_activos = []
    for user in psutil.users():
        usuarios_activos.append({
            "Usuario": user.name,
            "Terminal": user.terminal,
            "Host": user.host,
            "Inicio de Sesión": user.started
        })
    return usuarios_activos


def obtener_informacion_sesiones():
    informacion_sesiones = os.popen("w").read().strip().split("\n")
    return informacion_sesiones


def obtener_uso_recursos_por_usuario():
    uso_recursos_por_usuario = {}
    for process in psutil.process_iter(['pid', 'username', 'cpu_percent', 'memory_percent']):
        info = process.info
        username = info['username']
        cpu_percent = info['cpu_percent']
        memory_percent = info['memory_percent']

        if username in uso_recursos_por_usuario:
            uso_recursos_por_usuario[username]["Procesos"] += 1
            uso_recursos_por_usuario[username]["CPU"] += cpu_percent
            uso_recursos_por_usuario[username]["Memoria"] += memory_percent
        else:
            uso_recursos_por_usuario[username] = {
                "Procesos": 1,
                "CPU": cpu_percent,
                "Memoria": memory_percent
            }

    return uso_recursos_por_usuario



def main():
    print("\nUsuarios Activos:\n")
    tabla_usuarios = PrettyTable()
    tabla_usuarios.field_names = ["Usuario", "Terminal", "Host", "Inicio de Sesión"]
    usuarios_activos = obtener_usuarios_activos()
    for usuario in usuarios_activos:
        tabla_usuarios.add_row([
            usuario["Usuario"],
            usuario["Terminal"],
            usuario["Host"],
            usuario["Inicio de Sesión"]
        ])
    print(tabla_usuarios)

    print("\nInformación de Sesiones:\n")
    informacion_sesiones = obtener_informacion_sesiones()
    for sesion in informacion_sesiones:
        print(sesion)

    print("\n\nUso de Recursos por Usuario:\n")
    uso_recursos_por_usuario = obtener_uso_recursos_por_usuario()
    tabla_recursos = PrettyTable()
    tabla_recursos.field_names = ["Usuario", "Procesos", "Uso de CPU", "Uso de Memoria"]
    for usuario, recursos in uso_recursos_por_usuario.items():
        tabla_recursos.add_row([
            usuario,
            recursos["Procesos"],
            f"{recursos['CPU']:.2f}%",
            f"{recursos['Memoria']:.2f}%"
        ])
    print(tabla_recursos)



if __name__ == "__main__":
    main()

