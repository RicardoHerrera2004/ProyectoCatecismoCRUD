import json
import pyodbc


def crear_conexion():

    with open("configuracion.json", "r", encoding="utf-8") as f:
        datos_conexion = json.load(f)

    cfg = datos_conexion["sql_server"]
    server = cfg["name_server"]
    database = cfg["database"]
    username = cfg["user"]
    password = cfg["password"]
    driver = cfg["controlador_odbc"]   

    connection_string = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )

    return pyodbc.connect(connection_string)


def mostrar_opciones_crud():
    print("\n\t*************************************")  
    print("\t** SISTEMA CRUD CATECISMO - ALUMNOS **")  
    print("\t*************************************")  
    print("\tOpciones CRUD:\n")
    print("\t1. Consultar estudiantes")
    print("\t2. Insertar estudiante")
    print("\t3. Actualizar estudiante")
    print("\t4. Eliminar estudiante")
    print("\t5. Salir\n")


def consultar_estudiantes(conexion):
    try:
        print("\n\t\tLISTA DE ESTUDIANTES:\n")  

        SQL_QUERY = """
        SELECT PersonaID, Nombre, Apellido, Identificacion, Email, Telefono
        FROM Programas.VW_Estudiantes
        """

        cursor = conexion.cursor()
        cursor.execute(SQL_QUERY)
        records = cursor.fetchall()

        if not records:
            print("\tNo hay estudiantes registrados.")
            return

        print("ID\tNombre\t\tApellido\tIdentificación\t\tEmail\t\t\tTeléfono")
        print("-" * 100)
        for r in records:
            print(f"{r.PersonaID}\t{r.Nombre}\t{r.Apellido}\t{r.Identificacion}\t{r.Email}\t{r.Telefono}")
    
    except Exception as e:
        print("\n\tOcurrió un error al consultar estudiantes:\n\n", e)
    
    finally:
        print("\nProceso de consulta finalizado.\n")


def insertar_estudiante(conexion):
    try:
        cursor = conexion.cursor()
        print("\n\t\tINSERTAR ESTUDIANTE:\n")  

        print("Ingrese los datos del estudiante (formato fecha: AAAA-MM-DD):\n")
        nombre = input("Nombre: \t")
        apellido = input("Apellido: \t")
        tipo_doc = input("Tipo de documento (ej. CI, PAS): \t")
        nro_doc = input("Número de documento: \t")
        fecha_nac = input("Fecha de nacimiento (AAAA-MM-DD): \t")
        telefono = input("Teléfono: \t")
        email = input("Email: \t")
        fecha_bautismo = input("Fecha de bautismo (AAAA-MM-DD) [opcional]: \t")
        lugar_bautismo = input("Lugar de bautismo [opcional]: \t")
        observacion = input("Observación [opcional]: \t")

        fecha_bautismo = fecha_bautismo or None
        lugar_bautismo = lugar_bautismo or None
        observacion = observacion or None

        SENTENCIA_SQL = """
        EXEC Programas.SP_InsertarEstudiante
            ?,?,?,?,?,?,?,?,?,?
        """
        cursor.execute(
            SENTENCIA_SQL,
            (
                nombre,
                apellido,
                tipo_doc,
                nro_doc,
                fecha_nac,
                telefono,
                email,
                fecha_bautismo,
                lugar_bautismo,
                observacion
            )
        )

        resultado = cursor.fetchone()
        conexion.commit()

        if resultado:
            try:
                persona_id_creada = resultado.PersonaIdCreada
            except AttributeError:
                persona_id_creada = resultado[0]

            print(f"\nOk ... Inserción exitosa. PersonaId creado: {persona_id_creada}\n")
        else:
            print("\nOk ... Inserción ejecutada (no se recibió PersonaId).\n")

    except Exception as e:
        print("\n\tOcurrió un error al insertar estudiante:\n\n", e)

    finally:
        print("Proceso de inserción finalizado.\n")


def actualizar_estudiante(conexion):
    try:
        cursor = conexion.cursor()
        
        print("\n\tACTUALIZAR INFORMACIÓN DEL ESTUDIANTE:\n")
        persona_id = int(input("Ingrese PersonaId del estudiante: \t"))
        nombre = input("Nuevo nombre: \t")
        apellido = input("Nuevo apellido: \t")
        nro_doc = input("Nuevo número de documento: \t")
        telefono = input("Nuevo teléfono: \t")
        email = input("Nuevo email: \t")

        SENTENCIA_SQL = """
        EXEC Programas.SP_ActualizarEstudiante
            ?,?,?,?,?,?
        """

        cursor.execute(
            SENTENCIA_SQL,
            (
                persona_id,
                nombre,
                apellido,
                nro_doc,
                telefono,
                email
            )
        )
        
        conexion.commit()
        print("\nOk ... Actualización exitosa.\n")

    except Exception as e:
        print("\n\tOcurrió un error al actualizar estudiante:\n\n", e)
    finally:
        print("Proceso de actualización finalizado.\n")


def eliminar_estudiante(conexion):
    try:
        cursor = conexion.cursor()
        print("\n\tELIMINAR ESTUDIANTE:\n")  

        persona_id = int(input("Ingrese PersonaId del estudiante a eliminar: \t"))

        SENTENCIA_SQL = "EXEC Programas.SP_EliminarEstudiante ?"

        cursor.execute(SENTENCIA_SQL, (persona_id,))
        conexion.commit()

        print("\nOk ... Eliminación exitosa.\n")

    except Exception as e:
        print("\n\tOcurrió un error al eliminar estudiante:\n\n", e)
    finally:
        print("Proceso de eliminación finalizado.\n")


def main():
    conexion = None
    try:
        conexion = crear_conexion()
        print("\nConexión exitosa a la base de datos 'Catecismo'.\n")

        while True:
            mostrar_opciones_crud()
            opcion = input("Seleccione una opción 1-5:\t")
            
            if opcion == '1':
                consultar_estudiantes(conexion)
            elif opcion == '2':
                insertar_estudiante(conexion)
            elif opcion == '3':
                actualizar_estudiante(conexion)
            elif opcion == '4':
                eliminar_estudiante(conexion)
            elif opcion == '5':
                print("\nSaliendo del programa...\n")
                break
            else:
                print("\nOpción no válida.\n")   

    except Exception as e:
        print("\n\tOcurrió un error al conectar a SQL Server:\n\n", e)    

    finally:
        if conexion is not None:
            conexion.close()
        print("Conexión cerrada.\n")

if __name__ == "__main__":
    main()
