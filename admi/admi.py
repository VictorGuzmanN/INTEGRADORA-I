class Administrador:

    def __init__(self, usuario, contrasena, privilegios):
        self._usuario = usuario
        self._contrasena = contrasena
        self._privilegios = privilegios

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        self._usuario = valor

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor):
        self._contrasena = valor

    @property
    def privilegios(self):
        return self._privilegios

    @privilegios.setter
    def privilegios(self, valor):
        self._privilegios = valor

    def mostrar_datos(self):
        print(f"Usuario: {self.usuario}")
        print(f"Privilegios: {self.privilegios}")
        
    def editar_datos(self):
        print("Datos editados")
        
    def eliminar_datos(self):
        print("Datos eliminados")   
        
    def registrar_datos(self):
        print("Datos registrados")  
        
    def consultar_datos(self):
        print("Consultando datos")
        
    def buscar_datos(self):
        print("Buscando datos")
        
    def actualizar_datos(self):
        print("Actualizando datos")
    
    def listar_datos(self):
        print("Listando datos")
    
    def exportar_datos(self):
        print("Exportando datos")   
        
    def importar_datos(self):
        print("Importando datos")
        
    def respaldar_datos(self):
        print("Respaldando datos")

    def restaurar_datos(self):
        print("Restaurando datos")
        
    def eliminar_todo(self):
        print("Eliminando todos los datos")
    
    def eliminar_todo_usuario(self):
        print("Eliminando todos los datos de usuario")
    
    def eliminar_todo_privilegios(self):
        print("Eliminando todos los datos de privilegios")
        
    def eliminar_todo_contrasena(self):
        print("Eliminando todos los datos de contrasena")
        
    def eliminar_todo_usuario_privilegios(self):
        print("Eliminando todos los datos de usuario y privilegios")
        
    def eliminar_todo_usuario_contrasena(self):
        print("Eliminando todos los datos de usuario y contrasena")
        
    def eliminar_todo_privilegios_contrasena(self):
        print("Eliminando todos los datos de privilegios y contrasena")
        
    def eliminar_todo_usuario_privilegios_contrasena(self):
        print("Eliminando todos los datos de usuario, privilegios y contrasena")
        
    
        