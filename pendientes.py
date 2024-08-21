#!/usr/bin/env python3

from colorama import Fore as f
import argparse
import time
import csv 
import os.path
import os
# Use date module for dates


#Entradas:
#Editar
#eliminar

#En algún momento quiero agregarle detalles de prioridad y periodicidad.

#Por ejemplo, que al pasar cierto tiempo, las prioridades se actualizen.

home = os.path.expanduser("~")
data = home+"/.pendientes.csv"
### Setting up the parser and adding arguments 
parser = argparse.ArgumentParser()

parser.add_argument('-p', '--print', help="Imprime las tareas pendientes actuales", action="store_true")
parser.add_argument('-c', '--cli', help="Entra en modo CLI", action="store_true")
parser.add_argument('-rm', '--remove', help="Elimina una tarea especificada con palabras clave separadas por comas", action="store_true")
parser.add_argument('-i', '--insertar', help="Insertar tarea nueva", action="store_true")
parser.add_argument('-d', '--detalles', help="Imprimir detalles completos de una tarea existente", action="store_true")

args = parser.parse_args()

#Two methods for searching coincidences of a request
def coincidencia(lista: list, cadena: str) -> bool:
#    if len(cadena) == 0 or len(lista) ==0:
#        raise ValueError
    noncoincidence = False in [s.lower() in cadena.lower() for s in lista]
    return not noncoincidence 

def buscarCoincidencia(solicitudes: list) -> list:
    """Ingresas con una lista de palabras e imprimes los datos completos de la tarea si hay 
    sólo una coincidencia, la sublista de tareas con las que coincide las palabras (si hay 
    más de una coincidencia), o imprimes un error si no hay coincidencias."""
    tareas = []
    with open(data, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "tarea": continue
            if coincidencia(solicitudes, row[1]):
                tareas.append(row)
    return tareas

#Printing methods
def imprimirArbol() -> None:
    arbol = []
    with open(data, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            arbol.append("+ "+row[1])
    print('\n'.join(arbol[1:]))

def imprimirsubLista(tareas: list) -> None:
    print('\n'.join(["+ "+tarea[1] for tarea in tareas]))


def imprimirDetalles() -> None:
    solicitudes = input('Palabras clave: ').split(', ')
    tareas = buscarCoincidencia(solicitudes)
    try:
        if len(tareas) > 1: 
            print('¿Puedes ser más específico?')
            imprimirsubLista(tareas)
            imprimirDetalles()
        else:
            print('\n'.join(tareas[0]))
    except IndexError: 
        print(f'No existe ninguna tarea que coincida con tu petición')

def insertarTarea() -> None:
    existenceofFile = os.path.isfile(data)
    with open(data, 'a', newline='') as csvfile:
        fieldnames = ["prioridad","tarea","descripción","fecha límite", "categoría"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not existenceofFile:
            writer.writeheader()
        fieldData = dict()
        for field in fieldnames:
            fieldData[field] = input(field+': ')
        writer.writerow(fieldData)

def eliminarTarea() -> None:
    solicitudes = input('Palabras clave: ').split(', ')
    tareas = buscarCoincidencia(solicitudes)
    try:
        if len(tareas) > 1:
            print("¿Cuál de los siguientes pendientes quieres eliminar?")
            imprimirsubLista(tareas)
            eliminarTarea()
        else:
            tarea = tareas[0]
            titulo = tarea[1]
            print(f'Tarea "{tarea[1]}" elmininada')
            with open(data, 'r') as f:
                lines = f.readlines()
            with open(data, 'w') as f:
                for line in lines:
                    nuevo_titulo = line.split(',')[1]
                    if nuevo_titulo != titulo:
                        f.write(line)
    except IndexError:
        print('No existe ninguna tarea pendiente con esas palabras clave')


def editarTarea() -> None:
    pass

def clear() -> None:
    os.system('clear')
    print(f"""{f.YELLOW}
    (print) Imprimir lista de tareas pendientes
    (remove) Eliminar un pendiente
    (insert) Insertar pendiente
    (details) Imprimir detalles de pendiente
    (exit) Salir del menu
    (clear) Clear screen
    """)

def cli() -> None:
    help_msg = f"""{f.YELLOW}
    (print) Imprimir lista de tareas pendientes
    (remove) Eliminar un pendiente
    (insert) Insertar pendiente
    (details) Imprimir detalles de pendiente
    (exit) Salir del menu
    (clear) Clear screen
    """
    print(help_msg)
    while True:
        option = input(f"  {f.YELLOW}[*] {f.CYAN}-> {f.WHITE}")
        if option == 'print': 
            imprimirArbol()
        if option == 'insert': 
            insertarTarea()
        if option == 'details': 
            imprimirDetalles()
        if option == 'remove':
            eliminarTarea()
        if option == 'exit':
            break
        if option == 'clear':
            clear()


def main() -> None:
    """"""
    if args.cli:
        cli()
    elif args.remove:
        eliminarTarea()
    elif args.insertar:
        insertarTarea()
    elif args.detalles:
        imprimirDetalles()
    else:
        imprimirArbol()
   
if __name__ == "__main__":
    main()
