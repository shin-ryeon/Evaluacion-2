
# Evaluación 2 — Cisco DevNet

## Descripción

Proyecto desarrollado en Python para integrar la API REST
de GraphHopper y realizar consultas de navegación.

El programa permite ingresar un origen y un destino,
consultar las coordenadas y obtener una ruta con
instrucciones en español.

## Tecnologías utilizadas

- Python 3
- Biblioteca requests
- API REST de GraphHopper
- JSON
- Cisco DEVASC
- Visual Studio Code

## Modificaciones implementadas

1. Interfaz y mensajes en español.
2. Distancias y tiempos con dos decimales.
3. Instrucciones de navegación en español mediante locale=es.
4. Salida escribiendo s o salir.
5. Manejo de errores HTTP y de conexión.
6. Protección de la API Key mediante getpass o variable de entorno.

## Requisitos

- Python 3 instalado.
- Biblioteca requests instalada.
- Conexión a Internet.
- API Key personal de GraphHopper.

Instalar requests:

    python3 -m pip install requests

## Ejecución

Ejecutar el programa:

    python3 graphhopper_parse-json_6.py

Cuando el programa solicite la API Key, introducir
una clave propia de GraphHopper.

La clave también puede configurarse mediante la
variable de entorno GRAPHHOPPER_API_KEY.

## Prueba de funcionamiento

Origen: Santiago, Chile

Destino: Valparaíso, Chile

Resultado obtenido durante la prueba:

- Código HTTP: 200
- Distancia: 120.06 km
- Distancia: 74.60 millas
- Tiempo estimado: 72.87 minutos
- Instrucciones de navegación: 13
- Idioma: español

Los resultados pueden variar según los datos de
rutas disponibles en GraphHopper.

## Seguridad

Este repositorio no incluye API Keys, contraseñas,
tokens, RUT ni archivos privados del laboratorio.

El programa solicita una clave GraphHopper propia
al momento de ejecutarse.

## Archivo principal

graphhopper_parse-json_6.py

## Contexto académico

Evaluación Parcial N.º 2 — Cisco DevNet.

Implementación basada en el flujo del laboratorio
de integración de una API REST en Python.
