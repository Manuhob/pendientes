#!/usr/bin/env python3

from colorama import Fore as f
import argparse
import time
import csv 
import os.path
import os

# Directorio del archivo principal donde se guardan los pendientes
home = os.path.expanduser("~")
data = home+"/.pendientes.csv"



### Agregar el parser de argumentos 
parser = argparse.ArgumentParser()

parser.add_argument('-p', '--print', help="Imprime las tareas pendientes actuales", action="store_true")
parser.add_argument('-c', '--cli', help="Entra en modo CLI", action="store_true")
parser.add_argument('-rm', '--remove', help="Elimina una tarea especificada con palabras clave separadas por comas", action="store_true")
parser.add_argument('-i', '--insertar', help="Insertar tarea nueva", action="store_true")
parser.add_argument('-e', '--editar', help="Editar tarea existente", action="store_true")
parser.add_argument('-d', '--detalles', help="Imprimir detalles completos de una tarea existente", action="store_true")
parser.add_argument('-cat', '--categoria', help="Imprimir sublista de tareas pendientes de cierta categoría", action="store")

args = parser.parse_args()


#Métodos de búsqueda de coincidencia de cadenas para solicitudes
def coincidencia(lista: list, cadena: str) -> bool:
    noncoincidence = False in [s.lower() in cadena.lower() for s in lista]
    return not noncoincidence 

def buscarCoincidencia(solicitudes: list) -> list:
    """Ingresas con una lista de palabras e imprimes los datos completos de la tarea si hay 
    sólo una coincidencia, la sublista de tareas con las que coincide las palabras (si hay 
    más de una coincidencia), o imprimes un error si no hay coincidencias."""
    tareas = [[],[]]
    with open(data, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "tarea": tareas[1] = row
            if coincidencia(solicitudes, row[1]):
                tareas[0].append(row)
    return tareas

#Métodos para imprimir información
def obtenerArbol() -> None:
    arbol = dict()
    with open(data, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "tarea": continue
            cat = row[-1].lower()
            name = "  + "+row[1]
            if cat in arbol.keys():
                arbol[cat] += [name]
            else: 
                arbol[cat] = [name]
    return arbol

def imprimirArbol() -> None:
    arbol = obtenerArbol()
    print('\nLista de pendientes actual: \n')
    for key in arbol:
        print(f'{key.upper()}:')
        print('\n'.join(arbol[key]))

def imprimirCategoria(key: str) -> None:
    arbol = obtenerArbol()
    try:
        print(f'\nPendientes de {key.upper()}:')
        print('\n'.join(arbol[key.lower()]))
    except KeyError:
        print(f'No existe una categoría con nombre {key}')

def imprimirsubLista(tareas: list) -> None:
    print('\n'.join(["+ "+tarea[1] for tarea in tareas]))


def imprimirDetalles() -> None:
    solicitudes = input('Palabras clave: ').split(', ')
    tareas,descripciones = buscarCoincidencia(solicitudes)
    try:
        if len(tareas) > 1: 
            print('¿Puedes ser más específico?')
            imprimirsubLista(tareas)
            imprimirDetalles()
        else:
            print('\n')
            for j in range(len(descripciones)):
                print(f'{descripciones[j].upper()}: {tareas[0][j]}')
    except IndexError: 
        print(f'No existe ninguna tarea que coincida con tu petición')

#Métodos de modificación de tareas
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
    tareas = buscarCoincidencia(solicitudes)[0]
    try:
        if len(tareas) > 1:
            print("¿Cuál de los siguientes pendientes quieres eliminar?")
            imprimirsubLista(tareas)
            eliminarTarea()
        else:
            tarea = tareas[0]
            titulo = tarea[1]
            with open(data, 'r') as f:
                lines = f.readlines()
            with open(data, 'w') as f:
                for line in lines:
                    nuevo_titulo = line.split(',')[1]
                    if nuevo_titulo != titulo:
                        f.write(line)
            print(f'Tarea "{tarea[1]}" eliminada')
    except IndexError:
        print('No existe ninguna tarea pendiente con esas palabras clave')


def editarTarea() -> None:
    solicitudes = input('Palabras clave: ').split(', ')
    tareas, descripciones = buscarCoincidencia(solicitudes)
    try:
        if len(tareas) > 1:
            print("¿Cuál de los siguientes pendientes quieres editar?")
            imprimirsubLista(tareas)
            editarTarea()
        else:
            # Imprimir tarea a editar
            tarea = tareas[0]
            print('\nTarea a editar:')
            for j in range(len(descripciones)):
                print(f'{descripciones[j].upper()}: {tareas[0][j]}')

            with open(data, 'r') as f:
                lines = f.readlines() #Lista de pendientes en cadena

            # Solicitar nueva información
            fieldData = [] 
            fieldnames = lines[0].split(',')
            print('\nNuevos datos')
            for field in fieldnames:
                fieldData.append(input(field.strip()+': '))
            nuevo_pendiente = ','.join(fieldData)+'\n'

            #Sobreescribir la información existente
            titulo = tarea[1]
            with open(data, 'w') as f:
                for line in lines:
                    nuevo_titulo = line.split(',')[1]
                    if nuevo_titulo != titulo:
                        f.write(line)
                    else:
                        f.write(nuevo_pendiente)
    except IndexError:
        print('No existe ninguna tarea pendiente con esas palabras clave') 

    #Métodos para interface de usuario 
def clear() -> None: 
    os.system('clear') 
    print(f"""{f.YELLOW}
            PENDIENTES

    Autor: Manuel Sedano Mendoza
    Licencia: MIT 
    Lenguaje: {f.CYAN} Python3{f.YELLOW}
    Descripción: Herramienta para manejar tareas pendientes

    Uso:
       (print) Imprimir lista de tareas pendientes
       (help) Mensaje de ayuda para otros comandos
    """)

def cli() -> None:
    author = f"""{f.YELLOW}
            PENDIENTES

    Autor: Manuel Sedano Mendoza
    Licencia: MIT 
    Lenguaje: {f.CYAN} Python3{f.YELLOW}
    Descripción: Herramienta para manejar tareas pendientes

    Uso:
       (print) Imprimir lista de tareas pendientes
       (help) Mensaje de ayuda para otros comandos
    """
    help_msg = f"""options:
        help            Muestra mensaje de ayuda
        print           Imprime las tareas pendientes actuales
        clear           Limpia la pantalla
        remove          Elimina una tarea especificada con palabras clave separadas por comas
        insert          Insertar tarea nueva
        details         Imprimir detalles completos de una tarea existente
        category        Imprimir sublista de tareas pendientes de cierta categoría"""
    print(author)
    while True:
        option = input(f"  {f.YELLOW}[*] {f.CYAN}-> {f.WHITE}")
        if option == 'help':
            print(help_msg)
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
        if option == 'category':
            imprimirCategoria(input("Nombre de categoria: "))


def main() -> None:
    if args.categoria:
        imprimirCategoria(args.categoria)
        return 
    if args.cli:
        cli()
    elif args.remove:
        eliminarTarea()
    elif args.insertar:
        insertarTarea()
    elif args.detalles:
        imprimirDetalles()
    elif args.editar:
        editarTarea()
    else:
        imprimirArbol()

   
if __name__ == "__main__":
    main()
