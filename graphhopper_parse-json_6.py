
# EVALUACION 2 - GRAPHHOPPER
# Navegacion mediante API REST
# Adaptacion al español del laboratorio Cisco

import os
from getpass import getpass

import requests

BASE_URL = "https://graphhopper.com/api/1"
SALIDAS = {"s", "salir"}


def buscar_ubicacion(sesion, nombre, clave):
    """Convierte el nombre de un lugar a coordenadas."""

    respuesta = sesion.get(
        BASE_URL + "/geocode",
        params={
            "q": nombre,
            "locale": "es",
            "limit": 1,
            "key": clave
        },
        timeout=(10, 30)
    )

    respuesta.raise_for_status()
    datos = respuesta.json()

    lugares = datos.get("hits", [])

    if not lugares:
        raise ValueError(
            f"No se encontro la ubicacion: {nombre}"
        )

    lugar = lugares[0]
    punto = lugar.get("point", {})

    latitud = punto.get("lat")
    longitud = punto.get("lng")

    if latitud is None or longitud is None:
        raise ValueError(
            "La ubicacion no contiene coordenadas validas."
        )

    descripcion = ", ".join(
        str(valor) for valor in (
            lugar.get("name"),
            lugar.get("city"),
            lugar.get("state"),
            lugar.get("country")
        )
        if valor
    )

    print("Ubicacion encontrada:", descripcion)

    return f"{latitud},{longitud}", descripcion


def obtener_ruta(sesion, origen, destino, clave):
    """Consulta la API de rutas de GraphHopper."""

    parametros = [
        ("point", origen),
        ("point", destino),
        ("profile", "car"),
        ("locale", "es"),
        ("instructions", "true"),
        ("key", clave)
    ]

    respuesta = sesion.get(
        BASE_URL + "/route",
        params=parametros,
        timeout=(10, 45)
    )

    respuesta.raise_for_status()

    datos = respuesta.json()
    rutas = datos.get("paths", [])

    if not rutas:
        raise ValueError(
            "GraphHopper no devolvio una ruta disponible."
        )

    print("Estado de la API:", respuesta.status_code)

    return rutas[0]


def mostrar_ruta(ruta, nombre_origen, nombre_destino):
    """Muestra distancia, tiempo e instrucciones."""

    distancia_metros = float(ruta.get("distance", 0))
    tiempo_ms = float(ruta.get("time", 0))

    kilometros = distancia_metros / 1000
    millas = kilometros / 1.609344
    minutos = tiempo_ms / 60000

    print("\n" + "=" * 55)
    print("RESULTADO DE NAVEGACION")
    print("=" * 55)

    print("Origen:", nombre_origen)
    print("Destino:", nombre_destino)

    print(f"Distancia: {kilometros:.2f} km")
    print(f"Distancia: {millas:.2f} millas")
    print(f"Tiempo estimado: {minutos:.2f} minutos")

    print("\nINSTRUCCIONES DE NAVEGACION")
    print("-" * 55)

    instrucciones = ruta.get("instructions", [])

    if not instrucciones:
        print("La API no devolvio instrucciones.")
        return

    for numero, paso in enumerate(instrucciones, 1):
        texto = paso.get("text", "Instruccion no disponible")
        distancia = float(paso.get("distance", 0))

        km = distancia / 1000

        print(f"{numero}. {texto} ({km:.2f} km)")

    print("=" * 55)


def main():
    print("=" * 55)
    print(" SISTEMA DE NAVEGACION GRAPHHOPPER")
    print(" EVALUACION 2 - CISCO DEVNET")
    print("=" * 55)

    clave = os.environ.get(
        "GRAPHHOPPER_API_KEY", ""
    ).strip()

    if not clave:
        clave = getpass(
            "Introduce tu clave API de GraphHopper: "
        ).strip()

    if not clave:
        print("ERROR: Debes proporcionar una clave API.")
        return

    print("\nEscribe 's' o 'salir' para terminar.")

    with requests.Session() as sesion:
        sesion.headers["Accept"] = "application/json"

        while True:
            print("\n" + "-" * 55)

            origen = input(
                "Introduce la ubicacion de origen: "
            ).strip()

            if origen.lower() in SALIDAS:
                break

            if not origen:
                print("Debes escribir una ubicacion.")
                continue

            destino = input(
                "Introduce la ubicacion de destino: "
            ).strip()

            if destino.lower() in SALIDAS:
                break

            if not destino:
                print("Debes escribir un destino.")
                continue

            try:
                coordenadas_origen, nombre_origen = (
                    buscar_ubicacion(sesion, origen, clave)
                )

                coordenadas_destino, nombre_destino = (
                    buscar_ubicacion(sesion, destino, clave)
                )

                ruta = obtener_ruta(
                    sesion,
                    coordenadas_origen,
                    coordenadas_destino,
                    clave
                )

                mostrar_ruta(
                    ruta,
                    nombre_origen,
                    nombre_destino
                )

            except requests.exceptions.HTTPError as error:
                codigo = error.response.status_code

                print(f"\nError HTTP: {codigo}")

                if codigo in (401, 403):
                    print(
                        "Revisa tu clave API y sus permisos."
                    )
                else:
                    print(
                        "La API rechazo la solicitud."
                    )

            except requests.exceptions.RequestException:
                print(
                    "\nError de conexion con GraphHopper."
                )

            except (ValueError, KeyError, TypeError) as error:
                print("\nERROR:", error)

    print("\nPrograma finalizado correctamente.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado por el usuario.")
