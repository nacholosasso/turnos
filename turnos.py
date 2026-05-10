# Importamos 'firebase_admin' porque es la librería oficial que permite a nuestro código de Python comunicarse con la plataforma de Firebase.
import firebase_admin 

# De 'firebase_admin' traemos 'credentials' para poder comprobar nuestra identidad usando el archivo de seguridad JSON que descargamos.
from firebase_admin import credentials 

# También traemos 'firestore' porque es el tipo específico de base de datos (rápida y en la nube) que usaremos para guardar los turnos.
from firebase_admin import firestore 

# De la librería incorporada 'datetime' traemos 'datetime' (para crear y leer fechas) y 'timedelta' (para poder sumar o restar días fácilmente).
from datetime import datetime, timedelta 

# Creamos una variable llamada 'cred' que lee nuestro archivo secreto de Google Cloud para darnos permisos de administrador en la base de datos.
cred = credentials.Certificate('ruta/a/tu/archivo-clave.json') 

# Encendemos (inicializamos) la conexión principal con Firebase usando las credenciales que acabamos de cargar en el paso anterior.
firebase_admin.initialize_app(cred) 

# Creamos un cliente de Firestore (lo llamamos 'db' por "database") que será nuestra herramienta principal para enviar los datos a la nube.
db = firestore.client() 

# Definimos nuestra función principal llamada 'registrar_turno' que necesita recibir dos cosas: el nombre del 'barbero' y la 'fecha_str' (fecha en texto).
def registrar_turno(barbero, fecha_str):
    
    # Le indicamos a Python en qué formato específico escribiremos la fecha: "%Y" (Año), "%m" (mes), "%d" (día), separados por guiones.
    formato_fecha = "%Y-%m-%d" 
    
    # Iniciamos un bloque 'try'. Significa "intenta hacer esto". Lo usamos por si el usuario escribe mal la fecha y ocurre un error.
    try:
        
        # Convertimos el texto ('fecha_str') en un objeto de fecha real y matemático ('fecha_elegida') usando el formato que definimos.
        fecha_elegida = datetime.strptime(fecha_str, formato_fecha)
        
    # Si la conversión falla (se genera un ValueError porque el texto no era una fecha válida), atrapamos el error para que el programa no colapse.
    except ValueError:
        
        # Imprimimos un mensaje de error amigable en la consola explicando al usuario cómo debe ser escrito el texto.
        print("Error: Por favor usa el formato AAAA-MM-DD (Ejemplo: 2024-05-15) para la fecha.")
        
        # Usamos 'return' para detener la ejecución de toda la función aquí mismo, ya que sin una fecha correcta no podemos continuar.
        return
        
    # Obtenemos el momento y fecha exacta de este mismo instante usando el reloj de tu computadora y lo guardamos en la variable 'fecha_actual'.
    fecha_actual = datetime.now()
    
    # Calculamos cuál será la fecha límite en el futuro sumando 90 días (que equivalen a nuestros 3 meses) a la fecha de hoy.
    limite_tres_meses = fecha_actual + timedelta(days=90)
    
    # Preguntamos (con 'if') si la fecha que eligió el usuario es mayor, es decir, si está más allá en el futuro que nuestro límite de 3 meses.
    if fecha_elegida > limite_tres_meses:
        
        # Si la condición de arriba es cierta, le avisamos al usuario que está intentando reservar con demasiada anticipación.
        print("Error: No puedes sacar un turno a más de 3 meses de la fecha actual.")
        
        # Volvemos a usar 'return' para salir de la función, cancelando el proceso de guardado porque la regla no se cumplió.
        return
        
    # También preguntamos (con otro 'if') si la fecha elegida ya pasó, es decir, si es menor (más antigua) que la fecha de hoy.
    if fecha_elegida < fecha_actual:
        
        # Si es una fecha en el pasado, mostramos un error lógico, ya que no se pueden agendar cortes de pelo en días que ya ocurrieron.
        print("Error: La fecha elegida ya ha pasado.")
        
        # Usamos 'return' de nuevo para cancelar el proceso si la fecha es inválida por estar en el pasado.
        return
        
    # Si el código llegó hasta esta línea, significa que pasó todas las pruebas. Creamos un "diccionario" (datos emparejados en claves y valores).
    datos_turno = {
        # Guardamos el nombre del barbero ingresado y le ponemos la etiqueta "barbero" para que la base de datos sepa qué es.
        "barbero": barbero,
        # Guardamos el objeto de la fecha válida y le ponemos la etiqueta "fecha". Firestore entiende este formato perfectamente.
        "fecha": fecha_elegida
    }
    
    # Le decimos a nuestra base de datos ('db') que busque la colección o carpeta 'turnos' y que añada ('add') nuestro nuevo diccionario.
    db.collection('turnos').add(datos_turno)
    
    # Finalmente, imprimimos un mensaje de éxito en pantalla para confirmar que todo salió bien y el turno ya está en la nube.
    print(f"¡Éxito! El turno con el barbero {barbero} para la fecha {fecha_str} ha sido registrado.")


# EJEMPLOS DE USO:
# Para usar este sistema, solo debes borrar el símbolo # (para descomentar la línea) e invocar la función con los datos reales.
# registrar_turno("Carlos", "2026-06-25")
