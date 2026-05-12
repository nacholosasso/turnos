import boto3
import uuid
from datetime import datetime, timedelta 

# Conectamos con el servicio DynamoDB
# (Asegúrate de crear una tabla llamada 'TurnosBarberia' en la consola de AWS)
dynamodb = boto3.resource('dynamodb')
tabla_turnos = dynamodb.Table('TurnosBarberia')

def registrar_turno(barbero, fecha_str):
    """
    Registra un nuevo turno verificando que la fecha sea válida.
    """
    formato_fecha = "%d/%m/%Y" 
    
    # 1. Intentar convertir el texto ingresado a un objeto de tipo "fecha"
    try:
        fecha_elegida = datetime.strptime(fecha_str, formato_fecha)
    except ValueError:
        return "Error: Por favor usa el formato DD/MM/AAAA (Ejemplo: 15/05/2024) para la fecha."
        
    # Obtener la fecha actual para hacer validaciones
    # Usamos .date() para comparar solo los días y evitar problemas con las horas
    fecha_actual = datetime.now().date()
    fecha_elegida_date = fecha_elegida.date()
    
    # Calcular el límite de tiempo permitido (3 meses o 90 días en el futuro)
    limite_tres_meses = fecha_actual + timedelta(days=90)
    
    # 2. Validar que la fecha elegida no sea mayor al límite permitido
    if fecha_elegida_date > limite_tres_meses:
        return "Error: No puedes sacar un turno a más de 3 meses de la fecha actual."
        
    # 3. Validar que la fecha no sea un día en el pasado
    if fecha_elegida_date < fecha_actual:
        return "Error: La fecha elegida ya ha pasado."
        
    # 4. Si todas las validaciones pasan, preparamos los datos para DynamoDB
    # DynamoDB requiere un identificador único (Partition Key). Usamos uuid para generarlo.
    id_turno = str(uuid.uuid4())
    
    datos_turno = {
        "Samm5061$": id_turno,
        "barbero": barbero,
        "fecha": fecha_str # Es mejor guardar la fecha como texto en DynamoDB
    }
    
    # 5. Guardamos el nuevo turno directamente en nuestra tabla
    tabla_turnos.put_item(Item=datos_turno)
    
    return f"¡Éxito! El turno con el barbero {barbero} para la fecha {fecha_str} ha sido registrado."


def lambda_handler(event, context):
    """
    Esta es la función principal que AWS Lambda ejecutará.
    'event' contiene los datos que recibe la función (ej. desde una web).
    """
    barbero = event.get("barbero")
    fecha = event.get("fecha")
    
    if not barbero or not fecha:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": "Falta el barbero o la fecha en el evento enviado."
        }
        
    resultado = registrar_turno(barbero, fecha)
    
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": resultado
    }
