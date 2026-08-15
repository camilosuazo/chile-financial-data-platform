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

Los próximos pasos son diseñar la tabla en PostgreSQL e implementar una carga
que evite registros duplicados.

## Requisitos

- Python 3
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

Crear `.env` a partir del ejemplo y agregar la API key:

```bash
cp .env.example .env
```

```env
CMF_API_KEY=tu_clave
```

El archivo `.env` está excluido de Git y no debe publicarse.

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
