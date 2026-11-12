class Doctor:

    def __init__(self, nombre, especialidad, numero_cedula):
        self._nombre = nombre
        self._especialidad = especialidad
        self._numero_cedula = numero_cedula

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def especialidad(self):
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor):
        self._especialidad = valor

    @property
    def numero_cedula(self):
        return self._numero_cedula

    @numero_cedula.setter
    def numero_cedula(self, valor):
        self._numero_cedula = valor

    def atender_paciente(self):
        print("Paciente atendido")

    def generar_diagnostico(self):
        print("Diagnóstico generado")

    def asignar_tratamiento(self):
        print("Tratamiento asignado")