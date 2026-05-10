from datetime import datetime, timedelta 

# Lista que simula una base de datos para guardar los turnos
turnos_guardados = []

def registrar_turno(barbero, fecha_str):
    """
    Registra un nuevo turno verificando que la fecha sea válida.
    """
    formato_fecha = "%d/%m/%Y" 
    
    # 1. Intentar convertir el texto ingresado a un objeto de tipo "fecha"
    try:
        fecha_elegida = datetime.strptime(fecha_str, formato_fecha)
    except ValueError:
        print("Error: Por favor usa el formato DD/MM/AAAA (Ejemplo: 15/05/2024) para la fecha.")
        return # Sale de la función si hay error
        
    # Obtener la fecha actual para hacer validaciones
    fecha_actual = datetime.now()
    
    # Calcular el límite de tiempo permitido (3 meses o 90 días en el futuro)
    limite_tres_meses = fecha_actual + timedelta(days=90)
    
    # 2. Validar que la fecha elegida no sea mayor al límite permitido
    if fecha_elegida > limite_tres_meses:
        print("Error: No puedes sacar un turno a más de 3 meses de la fecha actual.")
        return
        
    # 3. Validar que la fecha no sea un día en el pasado
    if fecha_elegida < fecha_actual:
        print("Error: La fecha elegida ya ha pasado.")
        return
        
    # 4. Si todas las validaciones pasan, se crea un diccionario con los datos del turno
    datos_turno = {
        "barbero": barbero,
        "fecha": fecha_elegida
    }
    
    # Se añade el nuevo turno a nuestra lista (base de datos)
    turnos_guardados.append(datos_turno)
    
    print(f"¡Éxito! El turno con el barbero {barbero} para la fecha {fecha_str} ha sido registrado.")


# SISTEMA INTERACTIVO
# Este bloque se ejecuta si corremos el archivo directamente en la consola
if __name__ == "__main__":
    print("--- BIENVENIDO AL SISTEMA DE TURNOS ---")
    
    # Bucle infinito para mantener el menú abierto hasta que el usuario decida salir
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
                # Recorre la lista de turnos y muestra cada uno.
                # enumerate(..., 1) sirve para numerar la lista empezando por el 1.
                for i, turno in enumerate(turnos_guardados, 1):
                    # Volvemos a transformar la fecha en texto con un buen formato
                    fecha_bonita = turno['fecha'].strftime("%d/%m/%Y")
                    print(f"{i}. Barbero: {turno['barbero']} - Fecha: {fecha_bonita}")
                    
        else:
            print("Opción no válida. Por favor, ingresa 1, 2 o 3.")
