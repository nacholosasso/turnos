# De la librería incorporada 'datetime' traemos 'datetime' (para crear y leer fechas) y 'timedelta' (para poder sumar o restar días fácilmente).
from datetime import datetime, timedelta 

# Creamos una lista vacía que funcionará como base de datos en memoria para que puedas probar el código en Google Colab.
turnos_guardados = []

# Definimos nuestra función principal llamada 'registrar_turno' que necesita recibir dos cosas: el nombre del 'barbero' y la 'fecha_str' (fecha en texto).
def registrar_turno(barbero, fecha_str):
    
    # Le indicamos a Python en qué formato específico escribiremos la fecha: "%d" (día), "%m" (mes), "%Y" (Año), separados por barras.
    formato_fecha = "%d/%m/%Y" 
    
    # Iniciamos un bloque 'try'. Significa "intenta hacer esto". Lo usamos por si el usuario escribe mal la fecha y ocurre un error.
    try:
        
        # Convertimos el texto ('fecha_str') en un objeto de fecha real y matemático ('fecha_elegida') usando el formato que definimos.
        fecha_elegida = datetime.strptime(fecha_str, formato_fecha)
        
    # Si la conversión falla (se genera un ValueError porque el texto no era una fecha válida), atrapamos el error para que el programa no colapse.
    except ValueError:
        
        # Imprimimos un mensaje de error amigable en la consola explicando al usuario cómo debe ser escrito el texto.
        print("Error: Por favor usa el formato DD/MM/AAAA (Ejemplo: 15/05/2024) para la fecha.")
        
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
    
    # Guardamos el diccionario en nuestra lista (base de datos en memoria) para simular el almacenamiento.
    turnos_guardados.append(datos_turno)
    
    # Finalmente, imprimimos un mensaje de éxito en pantalla para confirmar que todo salió bien.
    print(f"¡Éxito! El turno con el barbero {barbero} para la fecha {fecha_str} ha sido registrado.")


# SISTEMA INTERACTIVO:
# Este bucle permite que el programa funcione continuamente en la consola de Visual Studio Code.
if __name__ == "__main__":
    print("--- BIENVENIDO AL SISTEMA DE TURNOS ---")
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Registrar un turno")
        print("2. Ver turnos guardados")
        print("3. Salir")
        opcion = input("Elige una opción (1, 2 o 3): ")
        
        if opcion == "3":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        elif opcion == "1":
            nombre_barbero = input("Ingresa el nombre del barbero: ")
            fecha_turno = input("Ingresa la fecha del turno (formato DD/MM/AAAA): ")
            registrar_turno(nombre_barbero, fecha_turno)
        elif opcion == "2":
            print("\n--- TURNOS REGISTRADOS ---")
            if not turnos_guardados:
                print("Aún no hay turnos registrados en el sistema.")
            else:
                # Recorremos la lista y mostramos cada turno con un formato de texto amigable
                for i, turno in enumerate(turnos_guardados, 1):
                    fecha_bonita = turno['fecha'].strftime("%d/%m/%Y")
                    print(f"{i}. Barbero: {turno['barbero']} - Fecha: {fecha_bonita}")
        else:
            print("Opción no válida. Por favor, ingresa 1, 2 o 3.")
