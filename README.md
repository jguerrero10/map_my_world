# Map My World API

**Map My World** es una API desarrollada con **FastAPI** para gestionar ubicaciones y categorías, y ofrecer recomendaciones de exploración basadas en combinaciones de ubicación-categoría que no han sido revisadas en los últimos 30 días.

## Tabla de Contenidos

- [Características Principales](#características-principales)
- [Modelos de Datos](#modelos-de-datos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Despliegue con Docker](#despliegue-con-docker)
- [Despliegue con Docker Compose (Opcional)](#despliegue-con-docker-compose-opcional)
- [Endpoints](#endpoints)
  - [Gestión de Ubicaciones y Categorías](#gestión-de-ubicaciones-y-categorías)
  - [Recomendaciones de Exploración](#recomendaciones-de-exploración)
  - [Registro de Revisiones](#registro-de-revisiones)
- [Pruebas](#pruebas)
- [Cobertura de Código](#cobertura-de-código)
- [Contribuir](#contribuir)

## Características Principales

- **Gestión de Ubicaciones y Categorías**: Permite añadir ubicaciones con latitud y longitud, y categorías como "restaurante", "parque", etc.
- **Recomendador de Exploración**: Sugiere combinaciones de ubicación-categoría que no han sido revisadas recientemente o que nunca han sido revisadas.
- **Registro de Revisiones**: Permite registrar la última revisión de una combinación específica de ubicación-categoría, actualizando la fecha de la última revisión para mantener las recomendaciones actualizadas.

## Modelos de Datos

### Ubicaciones (`locations`)
- **latitude**: Coordenada de latitud.
- **longitude**: Coordenada de longitud.

### Categorías (`categories`)
- **name**: Nombre de la categoría (e.g., "restaurante", "parque").

### Revisiones (`location_category_reviewed`)
- **location**: Ubicación.
- **category_id**: La categoría.
- **last_reviewed**: Fecha de la última revisión de la combinación es Nula por defecto.

## Instalación y Configuración

### Requisitos
- Python 3.10+
- MongoDB

### Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/jguerrero10/map_my_world.git
   cd map_my_world

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configura las variables de entorno necesarias en un archivo _.env_ (opcional si ya tienes configuraciones en MongoDB).
4. Ejecuta la aplicación:
   ```bash
   uvicorn app.main:app --reload
   ```
### Documentación de la API
FastAPI genera documentación automática que se puede ver en el navegador:

- **Swagger UI**: `http://127.0.0.1:8000/docs` - Proporciona una interfaz interactiva para probar los endpoints.
- **ReDoc**: `http://127.0.0.1:8000/redoc` - - Ofrece una vista de documentación más detallada y estructurada.

Accede a cualquiera de las dos para ver la descripción completa de los endpoints, modelos de datos, y probar la API directamente.

## Despliegue con Docker

Este proyecto incluye un archivo _Dockerfile_ para facilitar el despliegue en un contenedor de Docker.

1. Construye la imagen de Docker:
   ```bash
   docker build -t map-my-world .
   ```
2. Ejecuta el contenedor:
   ```bash
    docker run -d -p 8000:8000 map-my-world
    ```
3. Accede a la documentación de la API en `http://localhost:8000/docs` o `http://localhost:8000/redoc`.

## Despliegue con Docker Compose (Opcional)

El proyecto también incluye un archivo _docker-compose.yml_ para facilitar el despliegue de la API y una instancia de MongoDB en un solo comando.

1. Ejecuta el siguiente comando:
   ```bash
   docker-compose up -d
   ```
Esto ejecutará la aplicación y MongoDB juntos, haciendo que la API esté disponible en `http://localhost:8000/docs` o `http://localhost:8000/redoc`.

## Endpoints

### Gestión de Ubicaciones y Categorías
#### Añadir una Nueva Ubicación y su Categoría
- **URL**: `/review`
- **Método**: `POST`
- **Cuerpo de la Solicitud**:
    - **location**: Coordenadas de la ubicación (e.g., `{"latitude": 40.7128, "longitude": -74.0060}`).
    - **category**: Nombre de la categoría (e.g., `{"name": "restaurante"}`).
- **Respuesta Exitosa**:
- **Código de Estado**: `201 Created`
- **Cuerpo de la Respuesta**: La ubicación y la categoría añadidas.
- **Ejemplo**:
  ```json
  {
    "status": "Success",
     "data": [
    {
      "_id": "61f3b3b3b3b3b3b3b3b3b3b3",
      "location": {
        "latitude": 40.7128,
        "longitude": -74.0060
      },
      "category": {
        "name": "restaurante"
      }
  }
  ],
     "message": "Request processed successfully"
  }
  ```
#### Revise una Ubicación y su Categoría
- **URL**: `/review`
- **Método**: `PATCH`
- **Parámetros de la Solicitud**:
    - **location_id**: ID de la ubicación.
- **Respuesta Exitosa**:
- **Código de Estado**: `200 OK`
- **Cuerpo de la Respuesta**: La ubicación y la categoría revisadas.
- **Ejemplo**:
  ```json
  {
    "status": "Success",
     "data": [
    {
      "_id": "61f3b3b3b3b3b3b3b3b3b3",
      "location": {
        "latitude": 40.7128,
        "longitude": -74.0060
      },
      "category": {
        "name": "restaurante"
      }
  }
  ],
     "message": "Request processed successfully"
  }
  ```
### Recomendaciones de Exploración
#### Obtener Recomendaciones de Exploración
- **URL**: `//exploration-recommendations`
- **Método**: `GET`
- **Respuesta Exitosa**:
- **Código de Estado**: `200 OK`
- **Cuerpo de la Respuesta**: Una lista de combinaciones de ubicación-categoría recomendadas.
  - **Ejemplo**:
    ```json
        {
      "status": "Success",
      "data": [
          {
              "location": {
                  "latitude": 40.7128,
                  "longitude": -74.0060
              },
              "category": {
                  "name": "restaurante"
              }
          }
      ],
      "message": "Exploration recommendations retrieved successfully."
    }
  ```
### Coberura de Código

El proyecto usa _pytest-cov_ para medir la cobertura de código. La cobertura actual del código es del 100%, indicando que todos los módulos están completamente cubiertos por las pruebas.

Para ejecutar las pruebas y ver la cobertura de código, ejecuta el siguiente comando:
```bash
pytest --cov=app --cov-report=term-missing
```
#### Ejejmplo de Cobertura de Código
 ```plaintext
Name                                           Stmts   Miss  Cover   Missing
----------------------------------------------------------------------------
app/__init__.py                                    0      0   100%
app/database.py                                   10      0   100%
app/main.py                                        6      0   100%
app/models.py                                     33      0   100%
app/routes/__init__.py                             0      0   100%
app/routes/exploration_recommender_router.py      41      0   100%
app/routes/review_locations_router.py             15      0   100%
app/utils/__init__.py                              0      0   100%
app/utils/enums.py                                 4      0   100%
----------------------------------------------------------------------------
TOTAL                                            109      0   100%

 ```
