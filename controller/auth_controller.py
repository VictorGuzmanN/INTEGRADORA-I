import random
from database.conexion import ConexionBD
from model.administrador import Administrador


class AuthController:
    @staticmethod
    def iniciar_sesion(usuario, contrasena):
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return None
        try:
            cursor = conexion.cursor()
            sql = "SELECT id_admin, usuario, contrasena, privilegios FROM administrador WHERE usuario = %s AND contrasena = %s"
            cursor.execute(sql, (usuario, contrasena))
            fila = cursor.fetchone()
            if fila:
                return Administrador(
                    id_admin=fila[0],
                    usuario=fila[1],
                    contrasena=fila[2],
                    privilegios=fila[3]
                )
            return None
        except Exception as e:
            print(f"Error en iniciar_sesion: {e}")
            return None
        finally:
            conexion.close()

    @staticmethod
    def registrar_usuario(usuario, contrasena, rol, datos_extra=None):
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a la base de datos."
        datos_extra = datos_extra or {}
        try:
            cursor = conexion.cursor()

            # 1. Guardar credenciales en la tabla administrador
            sql_admin = "INSERT INTO administrador (usuario, contrasena, privilegios) VALUES (%s, %s, %s)"
            cursor.execute(sql_admin, (usuario, contrasena, rol))

            rol_limpio = rol.strip().lower()

            # 2. Si el rol es Doctor, insertar con sus datos completos
            if rol_limpio == "doctor":
                sql_doc = """INSERT INTO doctor 
                             (nombre, apellido1, apellido2, especialidad, numero_cedula, telefono, ciudad) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql_doc, (
                    datos_extra.get("nombre") or usuario,
                    datos_extra.get("apellido1", ""),
                    datos_extra.get("apellido2", ""),
                    datos_extra.get("especialidad", ""),
                    datos_extra.get("numero_cedula", ""),
                    datos_extra.get("telefono", ""),
                    datos_extra.get("ciudad", "")
                ))

            # 3. Si el rol es Paciente, insertar con sus datos completos
            elif rol_limpio == "paciente":
                sql_pac = """INSERT INTO paciente 
                             (nombre, apellido1, apellido2, telefono, tipo_sangre, alergias, estado_paciente) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql_pac, (
                    datos_extra.get("nombre") or usuario,
                    datos_extra.get("apellido1", ""),
                    datos_extra.get("apellido2", ""),
                    datos_extra.get("telefono", ""),
                    datos_extra.get("tipo_sangre", ""),
                    datos_extra.get("alergias") or "Ninguna",
                    datos_extra.get("estado_paciente") or "Registrado"
                ))

            conexion.commit()
            return True, f"Usuario '{usuario}' registrado correctamente con rol {rol}."
        except Exception as e:
            conexion.rollback()
            return False, f"Error al registrar usuario: {e}"
        finally:
            conexion.close()
    @staticmethod
    def obtener_usuarios():
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id_admin, usuario, privilegios FROM administrador")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            conexion.close()

    @staticmethod
    def solicitar_codigo_recuperacion(correo, usuario):
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a la base de datos.", None
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_admin FROM administrador WHERE usuario = %s", (usuario,))
            existe = cursor.fetchone()
            if not existe:
                return False, f"El usuario '{usuario}' no está registrado.", None

            codigo = str(random.randint(100000, 999999))
            return True, f"Se envió un código de verificación a {correo}.\n\n(Código de prueba: {codigo})", codigo
        except Exception as e:
            return False, f"Error al verificar cuenta: {e}", None
        finally:
            conexion.close()

    @staticmethod
    def restablecer_contrasena(usuario, nueva_contrasena):
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_admin FROM administrador WHERE usuario = %s", (usuario,))
            existe = cursor.fetchone()
            if not existe:
                return False, f"El usuario '{usuario}' no existe en el sistema."

            cursor.execute(
                "UPDATE administrador SET contrasena = %s WHERE usuario = %s",
                (nueva_contrasena, usuario)
            )
            conexion.commit()
            return True, f"Contraseña actualizada correctamente para '{usuario}'."
        except Exception as e:
            conexion.rollback()
            return False, f"Error al actualizar contraseña: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar_usuario(id_admin):
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT usuario, privilegios FROM administrador WHERE id_admin = %s", (id_admin,))
            dato = cursor.fetchone()

            cursor.execute("DELETE FROM administrador WHERE id_admin = %s", (id_admin,))
            eliminado = cursor.rowcount > 0

            if eliminado and dato:
                usuario, rol = dato
                if rol.strip().lower() == "doctor":
                    cursor.execute("DELETE FROM doctor WHERE nombre = %s", (usuario,))
                elif rol.strip().lower() == "paciente":
                    cursor.execute("DELETE FROM paciente WHERE nombre = %s", (usuario,))

            conexion.commit()
            if eliminado:
                return True, "Usuario eliminado correctamente de MySQL."
            return False, "No se encontró el usuario en la base de datos."
        except Exception as e:
            conexion.rollback()
            return False, f"Error al eliminar usuario en MySQL: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_admin):
        return AuthController.eliminar_usuario(id_admin)