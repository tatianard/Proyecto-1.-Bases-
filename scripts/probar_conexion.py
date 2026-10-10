from cassandra.cluster import Cluster
from cassandra.io.asyncioreactor import AsyncioConnection


class TraductorDireccion:
    def translate(self, address):
        if address == "172.18.0.2":
            return "127.0.0.1"
        return address


cluster = None

try:
    cluster = Cluster(
        ["127.0.0.1"],
        port=9042,
        connection_class=AsyncioConnection,
        address_translator=TraductorDireccion(),
        connect_timeout=5,
        control_connection_timeout=5,
    )

    print("Conectando con ScyllaDB...", flush=True)
    session = cluster.connect("aquasense")

    filas = session.execute(
        "SELECT keyspace_name FROM system_schema.keyspaces"
    )

    print("CONEXION CORRECTA", flush=True)
    print("Keyspaces encontrados:")

    for fila in filas:
        print("-", fila.keyspace_name)

except Exception as error:
    print("ERROR DE CONEXION:", repr(error), flush=True)

finally:
    if cluster is not None:
        cluster.shutdown()