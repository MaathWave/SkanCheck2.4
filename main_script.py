#!/usr/bin/env python3

import os
#import venv
import subprocess


def mostrar_banner():
	banner = """
    ░██████╗██╗░░██╗░█████╗░███╗░░██╗░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗
    ██╔════╝██║░██╔╝██╔══██╗████╗░██║██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝
    ╚█████╗░█████═╝░███████║██╔██╗██║██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░
    ░╚═══██╗██╔═██╗░██╔══██║██║╚████║██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░
    ██████╔╝██║░╚██╗██║░░██║██║░╚███║╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗
    ╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝

    *************************************************************************
    ***                  Bienvenidos a SkanCheck v2.4                     ***
    ***                                                                   ***
    ***      Herramienta para administracion de redes y sistemas          ***
    *************************************************************************
"""
	print(banner)

mostrar_banner()


#Crear entorno virtual para la ejecucion del script (asi no generar inconveniente con las bibliotecas o dependencias)
#********************************************************************************************************************
#****               Por el momento el entorno virtual estara sin funcionamiento, debido a                        ****
#****                                                                                                            ****
#****                varios errores que suceden en su ejecucion. Sera una mejora a futuro                        ****
#********************************************************************************************************************


#def crear_entorno_virtual():
#    venv_dir = os.path.join(os.getcwd(), "venv")
#    if not os.path.exists(venv_dir):
#        venv.create(venv_dir, with_pip=True)

#    activar_script = "Activar" if os.name == "nt" else "source venv/bin/Activar"
#    activar_cmd = f"{activar_script}"
#    subprocess.run(activar_cmd, shell=True, executable="/bin/bash", env=os.environ.copy())

#crear_entorno_virtual()




#Instalar las bibliotecas requeridas para la ejecucion de los scripts

def instalar_bibliotecas_requeridas(categoria):
    requisitos_path = os.path.join("scripts", categoria, "requisitos.txt")
    with open(requisitos_path, "r") as requisitos_file:
        required_libraries = requisitos_file.read().splitlines()
    for library in required_libraries:
        subprocess.run(["pip", "install", library])


#Ejecucion del script

def ejecutar_script(script_path):
    print(f"Ejecutando {script_path}...\n")
    subprocess.run(["python", script_path])
    print("\n")

def main():
    scripts_folder = "scripts"
    categorias = os.listdir(scripts_folder)

    print("Seleccione el script disponible que desea utilizar:")
    for i, category in enumerate(categorias, start=1):
        print(f"{i}. {category}")

    choice = int(input("\nSelecciona una categoría (número): ")) - 1

    if choice >= 0 and choice < len(categorias):
        category = categorias[choice]
        category_path = os.path.join(scripts_folder, category)
        scripts = os.listdir(category_path)

        print("\nScripts en la categoría seleccionada:")
        for i, script in enumerate(scripts, start=1):
            print(f"{i}. {script}")

        script_choice = int(input("\n ~ Selecciona un script (número): ")) - 1

        if script_choice >= 0 and script_choice < len(scripts):
            script_name = scripts[script_choice]
            script_path = os.path.join(category_path, script_name)

            instalar_bibliotecas_requeridas(category)

            ejecutar_script(script_path)
        else:
            print("\n ---Selección de script no válida.---")
    else:
        print("\n ---Selección de categoría no válida.---")



if __name__ == "__main__":
    main()


