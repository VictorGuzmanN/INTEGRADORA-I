from database.conexion import ConexionBD


class TratamientoController:
    @staticmethod
    def obtener_tratamientos():
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor(dictionary=True)
            sql = """SELECT t.id_tratamiento, t.id_doctor, t.id_paciente, 
                            CONCAT(d.nombre, ' ', d.apellido1) AS doctor,
                            CONCAT(p.nombre, ' ', p.apellido1) AS paciente,
                            CONCAT(d.id_doctor, ' - ', d.nombre, ' ', d.apellido1) AS doctor_nombre,
                            CONCAT(p.id_paciente, ' - ', p.nombre, ' ', p.apellido1) AS paciente_nombre,
                            t.fecha, t.hora, t.tratamiento, t.diagnostico_inicial, t.fecha_entrada
                     FROM tratamiento t
                     INNER JOIN doctor d ON t.id_doctor = d.id_doctor
                     INNER JOIN paciente p ON t.id_paciente = p.id_paciente"""
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener tratamientos: {e}")
            return []
        finally:
            conexion.close()

    @staticmethod
    def crear_tratamiento(id_doctor, id_paciente=None, fecha="", hora="", tratamiento="", diagnostico_inicial="", fecha_entrada=""):
        if hasattr(id_doctor, "id_doctor"):
            trat = id_doctor
            return TratamientoController.crear_tratamiento(
                trat.id_doctor, trat.id_paciente, trat.fecha, trat.hora,
                trat.tratamiento, trat.diagnostico_inicial, trat.fecha_entrada
            )

        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a MySQL."
        try:
            cursor = conexion.cursor()
            sql = """INSERT INTO tratamiento 
                     (id_doctor, id_paciente, fecha, hora, tratamiento, diagnostico_inicial, fecha_entrada) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (id_doctor, id_paciente, fecha, hora, tratamiento, diagnostico_inicial, fecha_entrada))
            cursor.execute("UPDATE paciente SET estado_paciente = 'En_Tratamiento' WHERE id_paciente = %s", (id_paciente,))
            conexion.commit()
            return True, "Tratamiento guardado correctamente."
        except Exception as e:
            conexion.rollback()
            return False, f"Error al guardar tratamiento: {e}"
        finally:
            conexion.close()

    @staticmethod
    def registrar_tratamiento(tratamiento):
        return TratamientoController.crear_tratamiento(tratamiento)

    @staticmethod
    def actualizar_tratamiento(id_tratamiento, id_doctor=None, id_paciente=None, fecha="", hora="", tratamiento="", diagnostico_inicial="", fecha_entrada=""):
        if hasattr(id_tratamiento, "id_tratamiento"):
            trat = id_tratamiento
            return TratamientoController.actualizar_tratamiento(
                trat.id_tratamiento, trat.id_doctor, trat.id_paciente, trat.fecha,
                trat.hora, trat.tratamiento, trat.diagnostico_inicial, trat.fecha_entrada
            )

        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a MySQL."
        try:
            cursor = conexion.cursor()
            sql = """UPDATE tratamiento SET id_doctor=%s, id_paciente=%s, fecha=%s, hora=%s, 
                     tratamiento=%s, diagnostico_inicial=%s, fecha_entrada=%s 
                     WHERE id_tratamiento=%s"""
            cursor.execute(sql, (id_doctor, id_paciente, fecha, hora, tratamiento, diagnostico_inicial, fecha_entrada, id_tratamiento))
            conexion.commit()
            return cursor.rowcount > 0, "Tratamiento actualizado correctamente."
        except Exception as e:
            conexion.rollback()
            return False, f"Error al actualizar tratamiento: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar_tratamiento(id_tratamiento):
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a MySQL."
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM tratamiento WHERE id_tratamiento = %s", (id_tratamiento,))
            conexion.commit()
            if cursor.rowcount > 0:
                return True, "Tratamiento eliminado correctamente de MySQL."
            return False, "No se encontró el tratamiento en la base de datos."
        except Exception as e:
            conexion.rollback()
            return False, f"Error al eliminar tratamiento: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_tratamiento):
        return TratamientoController.eliminar_tratamiento(id_tratamiento)