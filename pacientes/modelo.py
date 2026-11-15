# class Paciente:

#     def __init__(self, nombre, telefono, tipo_sangre):
#         self._nombre = nombre
#         self._telefono = telefono
#         self._tipo_sangre = tipo_sangre

#     @property
#     def nombre(self):
#         return self._nombre

#     @nombre.setter
#     def nombre(self, valor):
#         self._nombre = valor

#     @property
#     def telefono(self):
#         return self._telefono

#     @telefono.setter
#     def telefono(self, valor):
#         self._telefono = valor

#     @property
#     def tipo_sangre(self):
#         return self._tipo_sangre

#     @tipo_sangre.setter
#     def tipo_sangre(self, valor):
#         self._tipo_sangre = valor

#     def registrarse(self):
#         print("Paciente registrado")

#     def actualizar_datos(self):
#         print("Datos actualizados")

#     def consultar_diagnostico(self):
#         print("Consultando diagnóstico")


#MODELO
class Paciente:

    def __init__(self, nombre, telefono, tipo_sangre):
        self.nombre = nombre
        self.telefono = telefono
        self.tipo_sangre = tipo_sangre

    def mostrar_datos(self):
        return (
            f"Nombre: {self.nombre}\n"
            f"Teléfono: {self.telefono}\n"
            f"Tipo de sangre: {self.tipo_sangre}"
        )
        
    def editar_datos(self):
        print("Datos editados")
        
    def eliminar_datos(self):
        print("Datos eliminados")

    def eliminar_todo(self):
        print("Eliminando todos los datos del paciente")

    def eliminar_todo_nombre(self):
        print("Eliminando todos los datos de nombre")

    def eliminar_todo_telefono(self):
        print("Eliminando todos los datos de telefono")

    def eliminar_todo_tipo_sangre(self):
        print("Eliminando todos los datos de tipo de sangre")

    def eliminar_todo_nombre_telefono(self):
        print("Eliminando todos los datos de nombre y telefono")

    def eliminar_todo_nombre_tipo_sangre(self):
        print("Eliminando todos los datos de nombre y tipo de sangre")

    def eliminar_todo_telefono_tipo_sangre(self):
        print("Eliminando todos los datos de telefono y tipo de sangre")

    def eliminar_todo_nombre_telefono_tipo_sangre(self):
        print("Eliminando todos los datos de nombre, telefono y tipo de sangre")
        
        