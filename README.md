# Chile Financial Data Platform

Proyecto personal para aprender Data Engineering construyendo progresivamente
una plataforma de datos financieros chilenos.

La primera versión sigue un flujo deliberadamente sencillo:

```text
API de la CMF -> Python -> PostgreSQL
```

Por ahora, el único indicador considerado es la Unidad de Fomento (UF).

## Estado actual

- Entorno virtual de Python y dependencias mínimas.
- Configuración segura de la API key mediante variables de entorno.
- Extracción de valores mensuales de la UF desde la API de la CMF.
- Inspección inicial de la respuesta JSON.
- Transformación de fechas y valores a tipos adecuados para PostgreSQL.
- Tabla PostgreSQL con restricciones de integridad.
- Conexión e inserción desde Python mediante Psycopg.
- Carga idempotente que evita fechas duplicadas.
- Selección del año y mes que se desea cargar.

Los próximos pasos son incorporar logging, mejorar el manejo de errores y
permitir cargar rangos históricos.

## Requisitos

- Python 3
- PostgreSQL 18
- Una API key de la [CMF](https://api.cmfchile.cl/uso-de-api-key.html)

## Configuración local

Crear y activar un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Para desarrollar y ejecutar las pruebas, instalar las dependencias de
desarrollo (estas también incluyen las dependencias de ejecución):

```bash
python -m pip install -r requirements-dev.txt
```

Crear `.env` a partir del ejemplo y agregar la API key:

```bash
cp .env.example .env
```

```env
CMF_API_KEY=tu_clave
DB_NAME=chile_financial_data
DB_USER=tu_usuario_postgres
DB_HOST=localhost
DB_PORT=5432
```

El archivo `.env` está excluido de Git y no debe publicarse.

## Preparar PostgreSQL

Crear la base de datos:

```bash
createdb chile_financial_data
```

Crear las tablas:

```bash
psql -d chile_financial_data -f sql/create_tables.sql
```

## Ejecutar la extracción

Desde la raíz del proyecto:

```bash
python -m src.extract
```

Actualmente, el programa consulta los valores de la UF de enero de 2025 y
muestra la estructura general de la respuesta y el primer registro.

## Ejecutar la transformación

```bash
python -m src.transform
```

La transformación convierte las fechas a objetos `date` y los valores de la UF
a objetos `Decimal`.

## Ejecutar el pipeline completo

```bash
python -m src.main
```

Sin argumentos, el pipeline extrae los valores de enero de 2025. También se
puede elegir el período desde la terminal:

```bash
python -m src.main --year 2024 --month 12
```

El pipeline transforma los valores y los inserta en PostgreSQL. La fecha es la
clave primaria y la inserción utiliza
`ON CONFLICT DO NOTHING`, por lo que ejecutar nuevamente el pipeline no crea
duplicados.

Para ejecutar las pruebas:

```bash
python -m pytest
```

Para comprobar los datos cargados:

```bash
psql -d chile_financial_data -c "SELECT COUNT(*), MIN(observation_date), MAX(observation_date) FROM uf_values;"
```
