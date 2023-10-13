# MagicLinker: A Magical URL Shortener 🪄

MagicLinker es un acortador de URLs. Convierte URLs largos en enlaces cortos y manejables con un toque de magia.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos previos](#requisitos-previos)
- [Instalación y ejecución local](#instalación-y-ejecución-local)
- [Despliegue en AWS Lambda](#despliegue-en-aws-lambda)

## Características

- Acorta URLs.

## Configuración y despliegue

### Requisitos

- Python 3.10
- Node.js y Serverless Framework (para despliegue en AWS Lambda)
- Una instancia [PostgreSQL](https://www.elephantsql.com/)

### Instalación y ejecución local

#### Crea un entorno virtual:

```bash
python -m venv venv
```

#### Activación del entorno virtual

```bash
. ./venv/bin/activate
```

#### Instala las dependencias

```bash
pip install -r requirements.txt
```

#### Ejecuta la aplicación localmente:

```bash
python run.py
```

### Despliegue en AWS Lambda

1.- [Configura tus credenciales AWS](https://www.serverless.com/framework/docs/getting-started) y asegúrate de tener [Serverless Framework instalado](https://www.serverless.com/framework/docs/providers/aws/guide/credentials).

2.- Ejecuta el siguiente comando:

```bash
serverless deploy
```

3.- Navega a la consola de AWS y ve al servicio Lambda.

4.- Selecciona tu función (debería tener un nombre relacionado con tu proyecto, probablemente generado por Serverless Framework).

5.- En la pestaña "Configuración", haz clic en "Variables de entorno".

6.- Añade las siguientes variables:

BASE_URL: Esta es la URL que Serverless Framework te proporciona después de desplegar tu aplicación. Es la ruta base para acceder a tu aplicación en AWS Lambda.

DATABASE_URL: Esta es la URL de conexión a tu base de datos. Si estás utilizando un servicio como ElephantSQL, te proporcionarán esta URL.

7.- Haz clic en "Guardar" o "Aplicar" para guardar los cambios.

## Ejecución de las pruebas

Ejecuta pytest:

```bash
pytest ./tests/
```

Después de ejecutar las pruebas, pytest mostrará un resumen con las pruebas que pasaron y las que fallaron. Si hay fallos, podrás ver detalles sobre el error y en qué parte del código ocurrió.
