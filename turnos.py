import boto3
import json
import uuid
from datetime import datetime, timedelta 
from boto3.dynamodb.conditions import Attr

# Conectamos con el servicio DynamoDB
# (Asegúrate de crear una tabla llamada 'TurnosBarberia' en la consola de AWS)
dynamodb = boto3.resource('dynamodb')
tabla_turnos = dynamodb.Table('TurnosBarberia')

# Conectamos con el servicio de correos de AWS (Simple Email Service)
ses = boto3.client('ses', region_name='us-east-1')

def registrar_turno(barbero, fecha_str, hora_str, telefono, email):
    """
    Registra un nuevo turno verificando fecha y hora válidas, y envía un correo.
    """
    formato_fecha_hora = "%d/%m/%Y %H:%M" 
    
    # 1. Intentar convertir el texto ingresado a un objeto de tipo "fecha"
    try:
        fecha_hora_elegida = datetime.strptime(f"{fecha_str} {hora_str}", formato_fecha_hora)
    except ValueError:
        return "Error: Por favor usa el formato correcto de fecha (DD/MM/AAAA) y hora (HH:MM)."
        
    # Obtener la fecha y hora actual en Argentina (UTC -3)
    ahora_arg = datetime.utcnow() - timedelta(hours=3)
    
    # 2. Validar que la fecha no sea un día/hora en el pasado
    if fecha_hora_elegida < ahora_arg:
        return "Error: La fecha y hora elegidas ya han pasado."
    
    # Calcular el límite de tiempo permitido (1 mes o 30 días en el futuro)
    limite_un_mes = ahora_arg + timedelta(days=30)
    
    # 3. Validar que la fecha elegida no sea mayor al límite permitido
    if fecha_hora_elegida > limite_un_mes:
        return "Error: No puedes sacar un turno a más de 1 mes de la fecha actual."
        
    # 4. Validar que la hora sea en fracciones de 30 minutos
    if fecha_hora_elegida.minute not in (0, 30):
        return "Error: Los turnos solo se pueden reservar cada 30 minutos (ej. 10:00 o 10:30)."
        
    # 5. Validar que el turno no esté ocupado
    turnos_existentes = tabla_turnos.scan(
        FilterExpression=Attr('fecha').eq(fecha_str) & Attr('hora').eq(hora_str) & Attr('barbero').eq(barbero)
    )
    
    if turnos_existentes.get('Items'):
        return f"Error: {barbero} ya tiene un turno reservado el {fecha_str} a las {hora_str} hs. Por favor, elige otro horario."

    # 6. Si todas las validaciones pasan, preparamos los datos para DynamoDB
    # DynamoDB requiere un identificador único (Partition Key). Usamos uuid para generarlo.
    id_turno = str(uuid.uuid4())
    
    datos_turno = {
        "id_turno": id_turno,
        "barbero": barbero,
        "fecha": fecha_str,
        "hora": hora_str,
        "telefono": telefono,
        "email": email
    }
    
    # 7. Guardamos el nuevo turno directamente en nuestra tabla
    tabla_turnos.put_item(Item=datos_turno)
    
    # 8. Enviar correo de confirmación
    # Usamos tu Gmail verificado como remitente
    correo_remitente = "nacho.losasso@gmail.com" 
    
    try:
        ses.send_email(
            Source=correo_remitente,
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': 'Confirmación de tu turno - The Barber Shop'},
                'Body': {
                    'Text': {'Data': f'¡Hola!\n\nTu turno con {barbero} para el {fecha_str} a las {hora_str} hs ha sido confirmado con éxito.\n\nTe esperamos,\nThe Barber Shop.'}
                }
            }
        )
        mensaje_correo = " y te hemos enviado un correo de confirmación."
    except Exception as e:
        print("Error al enviar el correo:", e)
        mensaje_correo = " (El turno se guardó, pero hubo un error al enviar el correo. Verifica tu configuración de SES)."

    return f"¡Éxito! El turno con {barbero} para el {fecha_str} a las {hora_str} hs ha sido registrado{mensaje_correo}"


def lambda_handler(event, context):
    """
    Esta es la función principal que AWS Lambda ejecutará.
    'event' contiene los datos que recibe la función (ej. desde una web).
    """
    
    # Si la petición viene desde una web (API Gateway/Function URL), los datos vienen como texto JSON dentro de "body"
    if "body" in event and event["body"]:
        body = json.loads(event["body"])
        barbero = body.get("barbero")
        fecha = body.get("fecha")
        hora = body.get("hora")
        telefono = body.get("telefono")
        email = body.get("email")
    else:
        # Para pruebas directas desde la consola de Lambda
        barbero = event.get("barbero")
        fecha = event.get("fecha")
        hora = event.get("hora")
        telefono = event.get("telefono")
        email = event.get("email")
    
    if not barbero or not fecha or not hora or not telefono or not email:
        return {
            "statusCode": 400,
            "body": "Faltan datos obligatorios en el formulario (barbero, fecha, hora, teléfono o email)."
        }
        
    resultado = registrar_turno(barbero, fecha, hora, telefono, email)
    
    return {
        "statusCode": 200,
        "body": resultado
    }
