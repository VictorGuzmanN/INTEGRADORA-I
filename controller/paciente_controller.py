from database.conexion import ConexionBD


class PacienteController:
    @staticmethod
    def obtener_pacientes():
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""SELECT id_paciente, nombre, apellido1, apellido2, telefono, calle, numero, 
                                     colonia, ciudad, estado, codigo_postal, tipo_sangre, alergias, estado_paciente 
                              FROM paciente""")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener pacientes: {e}")
            return []
        finally:
            conexion.close()

    @staticmethod
    def crear_paciente(nombre, apellido1="", apellido2="", telefono="", calle="", numero="", colonia="", ciudad="", estado="", codigo_postal="", tipo_sangre="", alergias="", estado_paciente="Registrado"):
        if hasattr(nombre, "nombre"):
            pac = nombre
            return PacienteController.crear_paciente(
                pac.nombre, pac.apellido1, pac.apellido2, pac.telefono,
                pac.calle, pac.numero, pac.colonia, pac.ciudad, pac.estado,
                pac.codigo_postal, pac.tipo_sangre, pac.alergias, pac.estado_paciente
            )

        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a MySQL."
        try:
            cursor = conexion.cursor()
            estado_final = estado_paciente.strip() if estado_paciente and estado_paciente.strip() != "" else "Registrado"
            sql = """INSERT INTO paciente 
                     (nombre, apellido1, apellido2, telefono, calle, numero, colonia, ciudad, estado, codigo_postal, tipo_sangre, alergias, estado_paciente) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nombre, apellido1, apellido2, telefono, calle, numero, colonia, ciudad, estado, codigo_postal, tipo_sangre, alergias, estado_final))
            conexion.commit()
            return True, "Paciente registrado correctamente."
        except Exception as e:
            conexion.rollback()
            return False, f"Error al registrar paciente: {e}"
        finally:
            conexion.close()

    @staticmethod
    def registrar_paciente(paciente):
        return PacienteController.crear_paciente(paciente)

    @staticmethod
    def actualizar_paciente(id_paciente, nombre="", apellido1="", apellido2="", telefono="", calle="", numero="", colonia="", ciudad="", estado="", codigo_postal="", tipo_sangre="", alergias="", estado_paciente="Registrado"):
        if hasattr(id_paciente, "id_paciente"):
            pac = id_paciente
            return PacienteController.actualizar_paciente(
                pac.id_paciente, pac.nombre, pac.apellido1, pac.apellido2, pac.telefono,
                pac.calle, pac.numero, pac.colonia, pac.ciudad, pac.estado,
                pac.codigo_postal, pac.tipo_sangre, pac.alergias, pac.estado_paciente
            )

        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a MySQL."
        try:
            cursor = conexion.cursor()
            sql = """UPDATE paciente SET nombre=%s, apellido1=%s, apellido2=%s, telefono=%s, calle=%s, numero=%s, 
                     colonia=%s, ciudad=%s, estado=%s, codigo_postal=%s, tipo_sangre=%s, alergias=%s, estado_paciente=%s 
                     WHERE id_paciente=%s"""
            cursor.execute(sql, (nombre, apellido1, apellido2, telefono, calle, numero, colonia, ciudad, estado, codigo_postal, tipo_sangre, alergias, estado_paciente, id_paciente))
            conexion.commit()
            return cursor.rowcount > 0, "Paciente actualizado correctamente."
        except Exception as e:
            conexion.rollback()
            return False, f"Error al actualizar paciente: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar_paciente(id_paciente):
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a MySQL."
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM paciente WHERE id_paciente = %s", (id_paciente,))
            conexion.commit()
            if cursor.rowcount > 0:
                return True, "Paciente eliminado correctamente de MySQL."
            return False, "No se encontró el paciente en la base de datos."
        except Exception as e:
            conexion.rollback()
            return False, f"No se pudo eliminar (verifica que no tenga tratamientos activos): {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_paciente):
        return PacienteController.eliminar_paciente(id_paciente)