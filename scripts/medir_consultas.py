import csv
import math
import statistics
import time
from datetime import date, datetime
from pathlib import Path

from cassandra.cluster import Cluster
from cassandra.io.asyncioreactor import AsyncioConnection


REPETICIONES = 30
CALENTAMIENTO = 5
CARPETA_RESULTADOS = Path("resultados")


class TraductorDireccion:
    def translate(self, address):
        if address == "172.18.0.2":
            return "127.0.0.1"
        return address


def medir_consulta(session, nombre, consulta, parametros):
    tiempos_ms = []
    filas_obtenidas = 0

    preparada = session.prepare(consulta)

    # Ejecuciones iniciales para reducir el efecto
    # de la primera conexión y la preparación.
    for _ in range(CALENTAMIENTO):
        resultado = session.execute(preparada, parametros)
        filas_obtenidas = len(list(resultado))

    # Mediciones de latencia.
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()

        resultado = session.execute(preparada, parametros)
        filas = list(resultado)

        fin = time.perf_counter()

        tiempos_ms.append((fin - inicio) * 1000)
        filas_obtenidas = len(filas)

    tiempos_ordenados = sorted(tiempos_ms)
    indice_p95 = math.ceil(0.95 * len(tiempos_ordenados)) - 1

    resultado = {
        "consulta": nombre,
        "repeticiones": REPETICIONES,
        "filas_de_ultima_consulta": filas_obtenidas,
        "mediana_ms": round(statistics.median(tiempos_ms), 3),
        "p95_ms": round(tiempos_ordenados[indice_p95], 3),
        "minimo_ms": round(min(tiempos_ms), 3),
        "maximo_ms": round(max(tiempos_ms), 3),
    }

    print(f"\nConsulta: {nombre}")
    print(f"Filas devueltas: {filas_obtenidas}")
    print(f"Mediana: {resultado['mediana_ms']} ms")
    print(f"P95: {resultado['p95_ms']} ms")
    print(f"Mínimo: {resultado['minimo_ms']} ms")
    print(f"Máximo: {resultado['maximo_ms']} ms")

    return resultado


def main():
    CARPETA_RESULTADOS.mkdir(parents=True, exist_ok=True)

    cluster = None
    resultados = []

    try:
        cluster = Cluster(
            ["127.0.0.1"],
            port=9042,
            connection_class=AsyncioConnection,
            address_translator=TraductorDireccion(),
            connect_timeout=10,
            control_connection_timeout=10,
        )

        session = cluster.connect("aquasense")
        print("Conexion correcta con ScyllaDB.")
        print(f"Repeticiones por consulta: {REPETICIONES}")
        print(f"Calentamiento por consulta: {CALENTAMIENTO}")

        # 1. Últimas mediciones de un sensor.
        resultados.append(medir_consulta(
            session,
            "ultimas_mediciones_sensor",
            """
            SELECT sensor_id, timestamp, caudal, presion
            FROM mediciones_por_sensor
            WHERE sensor_id = ? AND mes_anio = ?
            LIMIT 20
            """,
            ("S0001", "2026-01"),
        ))

        # 2. Intervalo temporal de un sensor.
        resultados.append(medir_consulta(
            session,
            "intervalo_temporal_sensor",
            """
            SELECT sensor_id, timestamp, caudal, presion
            FROM mediciones_por_sensor
            WHERE sensor_id = ? AND mes_anio = ?
              AND timestamp >= ? AND timestamp < ?
            LIMIT 100
            """,
            (
                "S0001",
                "2026-01",
                datetime(2026, 1, 1),
                datetime(2026, 1, 3),
            ),
        ))

        # 3. Zona durante un intervalo temporal.
        resultados.append(medir_consulta(
            session,
            "intervalo_temporal_zona",
            """
            SELECT zona_id, timestamp, sensor_id, caudal, presion
            FROM mediciones_por_zona
            WHERE zona_id = ? AND mes_anio = ?
              AND timestamp >= ? AND timestamp < ?
            LIMIT 100
            """,
            (
                "Z01",
                "2026-01",
                datetime(2026, 1, 1),
                datetime(2026, 1, 2),
            ),
        ))

        # 4. Resumen diario de una zona.
        resultados.append(medir_consulta(
            session,
            "resumen_diario_zona",
            """
            SELECT zona_id, fecha, total_mediciones,
                   total_anomalias, presion_maxima
            FROM resumen_diario_zona
            WHERE zona_id = ? AND fecha >= ? AND fecha <= ?
            LIMIT 31
            """,
            (
                "Z01",
                date(2026, 1, 1),
                date(2026, 2, 11),
            ),
        ))

        archivo_salida = (
            CARPETA_RESULTADOS / "rendimiento_consultas.csv"
        )

        with open(
            archivo_salida,
            "w",
            newline="",
            encoding="utf-8",
        ) as archivo:
            campos = list(resultados[0].keys())
            escritor = csv.DictWriter(
                archivo,
                fieldnames=campos,
            )
            escritor.writeheader()
            escritor.writerows(resultados)

        print("\nPruebas de rendimiento terminadas.")
        print(f"Resultados guardados en: {archivo_salida}")

    finally:
        if cluster is not None:
            cluster.shutdown()


if __name__ == "__main__":
    main()