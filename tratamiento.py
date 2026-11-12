class Tratamiento:

    def __init__(self, fecha, tratamiento, diagnostico_inicial):
        self._fecha = fecha
        self._tratamiento = tratamiento
        self._diagnostico_inicial = diagnostico_inicial

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor

    @property
    def tratamiento(self):
        return self._tratamiento

    @tratamiento.setter
    def tratamiento(self, valor):
        self._tratamiento = valor

    @property
    def diagnostico_inicial(self):
        return self._diagnostico_inicial

    @diagnostico_inicial.setter
    def diagnostico_inicial(self, valor):
        self._diagnostico_inicial = valor

    def registrar_tratamiento(self):
        print("Tratamiento registrado")

    def actualizar_tratamiento(self):
        print("Tratamiento actualizado")

    def consultar_tratamiento(self):
        print("Consultando tratamiento")

    def eliminar_tratamiento(self):
        print("Tratamiento eliminado")