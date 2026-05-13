# 💈 The Barber Shop - Sistema de Turnos Serverless

Este es un proyecto completo de reserva de turnos para una barbería, construido utilizando una arquitectura 100% Serverless en Amazon Web Services (AWS). Permite a los clientes elegir un barbero, seleccionar una fecha y hora, y recibir automáticamente un correo de confirmación si el horario está disponible.

## 🚀 Arquitectura y Servicios de AWS

El sistema hace uso intensivo del ecosistema de AWS para garantizar escalabilidad, alta disponibilidad y bajo costo:

- **Amazon S3**: Utilizado para el hosting estático del frontend (`index.html`).
- **AWS Lambda**: Contiene la lógica de negocio (`turnos.py`). Expone una *Function URL* para ser consumida directamente desde el frontend y procesar las reservas.
- **Amazon DynamoDB**: Base de datos NoSQL que almacena la información de los turnos en la tabla `TurnosBarberia`.
- **Amazon Simple Email Service (SES)**: Encargado de despachar los correos electrónicos de confirmación a los usuarios de forma automática.
- **AWS IAM (Identity and Access Management)**: Gestiona los roles y permisos necesarios de ejecución para que la función Lambda pueda leer/escribir en DynamoDB y enviar correos mediante SES.
- **AWS Database Migration Service (DMS)**: (Opcional/Planificado) Herramienta contemplada en el stack para facilitar la migración de datos históricos de turnos desde otras bases de datos relacionales o sistemas heredados hacia nuestra tabla nativa en DynamoDB.

## 📁 Estructura del Proyecto

```text
turnos/
│
├── index.html       # Interfaz de usuario (Frontend). Maneja validaciones de fecha y peticiones al backend.
├── turnos.py        # Código backend de la función Lambda (Python).
└── PY.txt           # Scripts útiles de PowerShell para despliegue en S3 y Lambda usando AWS CLI.
```

## ✨ Características Principales

- **Frontend Responsivo**: Formulario elegante con "Dark Mode" y acentos dorados.
- **Validación Inteligente de Fechas (Frontend y Backend)**: 
  - Bloqueo de fechas pasadas.
  - Límite de reservas a un máximo de 30 días en el futuro.
  - Generación de horarios en intervalos fijos de 30 minutos (09:00 a 20:00).
- **Verificación de Conflictos**: Evita el *double-booking* (doble reserva) consultando a la base de datos DynamoDB si el barbero ya está ocupado en la fecha y hora solicitadas.
- **Notificaciones Automáticas**: El cliente recibe un correo en su bandeja de entrada al confirmar la cita.

## 🛠️ Requisitos Previos

1. Cuenta activa en **AWS**.
2. **AWS CLI** instalado y configurado con credenciales de administrador (o permisos suficientes para S3 y Lambda).
3. **Python 3.12+** instalado localmente para empaquetado.
4. Tabla en DynamoDB creada con el nombre `TurnosBarberia`.
5. Correo electrónico verificado en Amazon SES (ej: `nacho.losasso@gmail.com`).

## 📦 Despliegue (Deploy)

El proyecto se divide en dos fases de despliegue, automatizables a través de la terminal (según se muestra en los scripts del archivo `PY.txt`):

### 1. Desplegar el Frontend (Amazon S3)

Asegúrate de que tu bucket de S3 (`turnos-barberia-ls`) esté configurado para **Static Website Hosting** y ejecuta:

```powershell
# Subir el archivo index.html al bucket S3
python -m awscli s3 cp index.html s3://turnos-barberia-ls
```

### 2. Desplegar el Backend (AWS Lambda)

El backend requiere ser comprimido en un archivo `.zip` antes de subirse.
Asegúrate de haber creado una función Lambda en AWS llamada `SistemaDeTurnos` utilizando Python 3.12 como *runtime*.

```powershell
# 1. Empaquetar el archivo Python
Compress-Archive -Path turnos.py -DestinationPath turnos.zip -Force

# 2. Actualizar el código de la función Lambda
python -m awscli lambda update-function-code --function-name SistemaDeTurnos --zip-file fileb://turnos.zip
```

### 3. Configuración Post-Despliegue

- **CORS**: Asegúrate de tener habilitado CORS en la *Function URL* de tu Lambda para permitir peticiones `POST` desde el dominio de S3.
- **Permisos IAM del Lambda Role**: El rol asociado a `SistemaDeTurnos` debe tener las políticas:
  - `AmazonDynamoDBFullAccess` (o permisos de escritura limitados a la tabla).
  - `AmazonSESFullAccess` (o `ses:SendEmail` permitido para la cuenta).

## 📝 Autor

Desarrollado para la gestión de **The Barber Shop**.