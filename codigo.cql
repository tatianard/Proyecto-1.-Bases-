CREATE KEYSPACE IF NOT EXISTS aquasense WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor': 1};

USE aquasense;

DROP TABLE IF EXISTS mediciones_por_sensor;
DROP TABLE IF EXISTS mediciones_por_zona;

CREATE TABLE IF NOT EXISTS mediciones_por_sensor (
    sensor_id text,
    mes_anio text, -- Columna de Bucketing, este se logra agrupando la fecha y el sensor y el mes de la partición
    timestamp timestamp,
    zona_id text,
    caudal double,
    presion double,
    temperatura double,
    calidad text,
    PRIMARY KEY ((sensor_id, mes_anio), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);


CREATE TABLE IF NOT EXISTS mediciones_por_zona (
    zona_id text,
    mes_anio text,
    timestamp timestamp,
    sensor_id text,
    caudal double,
    presion double,
    temperatura double,
    calidad text,
    PRIMARY KEY ((zona_id, mes_anio), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);
