from datetime import datetime

def registrar_respuesta(usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("respuesta.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha},USUARIO_BLOQUEADO,{usuario}\n")
    return fecha

intentos = {}

with open("eventos.log", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        partes = linea.strip().split(",")
        if len(partes) == 3:
            fecha, tipo, usuario = partes
            if tipo == "LOGIN_FALLIDO":
                if usuario not in intentos:
                    intentos[usuario] = []
                intentos[usuario].append(fecha)

for usuario, registros in intentos.items():
    if len(registros) >= 3:
        print("ALERTA DE SEGURIDAD")
        print("Usuario:", usuario)
        print("Intentos fallidos:", len(registros))
        print("Primer intento:", registros[0])
        print("Detección:", registros[2])
        
        fecha_respuesta = registrar_respuesta(usuario)
        print("Acción aplicada: bloqueo de usuario")
        print("Respuesta:", fecha_respuesta)
        
        inicio = datetime.strptime(registros[0], "%Y-%m-%d %H:%M:%S")
        deteccion = datetime.strptime(registros[2], "%Y-%m-%d %H:%M:%S")
        respuesta = datetime.strptime(fecha_respuesta, "%Y-%m-%d %H:%M:%S")
        
        mttr = (respuesta - deteccion).total_seconds()
        print("MTTR:", mttr, "segundos")
        
        mttd = (deteccion - inicio).total_seconds()
        print("MTTD:", mttd, "segundos")