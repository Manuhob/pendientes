# Pendientes

Esta es la primer versión de *pendientes*, un CLI escrito en Python3 para administrar tareas pendientes con 5 claves:
- Prioridad
- Título
- Descripción 
- Fecha límite
- Categoría

## Instalación
```bash
sudo wget https://raw.githubusercontent.com/Manuhob/pendientes/main/pendientes.py -O /usr/local/bin/pendientes
sudo chmod a+rx /usr/local/bin/pendientes
```

## Uso

Para imprimir la lista actual de tareas pendientes se teclea simplemente 
```Python3
pendientes 
```

Para imprimir detalles de una tarea, se teclea
```Python3
pendientes -d
```
lo cual despliega una entrada de texto, en la cual se pueden teclear palabras clave de la tarea, separadas por comas.

El  CLI tiene una interface con descripción de comandos a la cual se puede acceder con el comando 
```Python3
pendientes -c
```

Para más información, usar el comando
```Python3
pendientes --help
```

## Advertencia
Esta es una primer versión con varios fallos, por lo que aún no es demasiado estable y su presentación deja bastante qué desear.
