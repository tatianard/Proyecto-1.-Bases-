CREATE KEYSPACE IF NOT EXISTS aquasense WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor': 1};

USE aquasense;

CREATE TABLE IF NOT EXISTS mediciones_por_sensor (
    sensor_id text,
    timestamp timestamp,
    zona_id text,
    caudal double,
    presion double,
    temperatura double,
    calidad text,
    PRIMARY KEY ((sensor_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);


CREATE TABLE IF NOT EXISTS mediciones_por_zona (
    zona_id text,
    timestamp timestamp,
    sensor_id text,
    caudal double,
    presion double,
    temperatura double,
    calidad text,
    PRIMARY KEY ((zona_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);
