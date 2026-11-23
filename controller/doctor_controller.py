from database.conexion import ConexionBD


class DoctorController:
    @staticmethod
    def obtener_doctores():
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""SELECT id_doctor, nombre, apellido1, apellido2, especialidad, numero_cedula, 
                                     telefono, calle, numero, colonia, ciudad, estado, codigo_postal 
                              FROM doctor""")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener doctores: {e}")
            return []
        finally:
            conexion.close()

    @staticmethod
    def crear_doctor(nombre, apellido1, apellido2="", especialidad="", numero_cedula="", telefono="", calle="", numero="", colonia="", ciudad="", estado="", codigo_postal=""):
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a MySQL."
        try:
            cursor = conexion.cursor()
            sql = """INSERT INTO doctor 
                     (nombre, apellido1, apellido2, especialidad, numero_cedula, telefono, calle, numero, colonia, ciudad, estado, codigo_postal) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nombre, apellido1, apellido2, especialidad, numero_cedula, telefono, calle, numero, colonia, ciudad, estado, codigo_postal))
            conexion.commit()
            return True, "Doctor registrado correctamente."
        except Exception as e:
            conexion.rollback()
            return False, f"Error al registrar doctor: {e}"
        finally:
            conexion.close()

    @staticmethod
    def actualizar_doctor(id_doctor, nombre, apellido1, apellido2="", especialidad="", numero_cedula="", telefono="", calle="", numero="", colonia="", ciudad="", estado="", codigo_postal=""):
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a MySQL."
        try:
            cursor = conexion.cursor()
            sql = """UPDATE doctor SET nombre=%s, apellido1=%s, apellido2=%s, especialidad=%s, numero_cedula=%s, 
                     telefono=%s, calle=%s, numero=%s, colonia=%s, ciudad=%s, estado=%s, codigo_postal=%s 
                     WHERE id_doctor=%s"""
            cursor.execute(sql, (nombre, apellido1, apellido2, especialidad, numero_cedula, telefono, calle, numero, colonia, ciudad, estado, codigo_postal, id_doctor))
            conexion.commit()
            return cursor.rowcount > 0, "Doctor actualizado correctamente."
        except Exception as e:
            conexion.rollback()
            return False, f"Error al actualizar doctor: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar_doctor(id_doctor):
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a MySQL."
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM doctor WHERE id_doctor = %s", (id_doctor,))
            conexion.commit()
            if cursor.rowcount > 0:
                return True, "Doctor eliminado correctamente de MySQL."
            return False, "No se encontró el doctor en la base de datos."
        except Exception as e:
            conexion.rollback()
            return False, f"No se pudo eliminar (verifica que no tenga tratamientos activos): {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_doctor):
        return DoctorController.eliminar_doctor(id_doctor)