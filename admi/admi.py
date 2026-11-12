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