class Paciente:
    def __init__(self, nombre, apellido1, apellido2, telefono, tipo_sangre,
                 alergias="Ninguna", calle="", numero="", colonia="", ciudad="",
                 estado="", codigo_postal="", estado_paciente="Registrado", id_paciente=None):
        self._id_paciente = id_paciente
        self._nombre = nombre
        self._apellido1 = apellido1
        self._apellido2 = apellido2
        self._telefono = telefono
        self._tipo_sangre = tipo_sangre
        self._alergias = alergias
        self._calle = calle
        self._numero = numero
        self._colonia = colonia
        self._ciudad = ciudad
        self._estado = estado
        self._codigo_postal = codigo_postal
        self._estado_paciente = estado_paciente

    @property
    def id_paciente(self):
        return self._id_paciente

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def apellido1(self):
        return self._apellido1

    @apellido1.setter
    def apellido1(self, valor):
        self._apellido1 = valor

    @property
    def apellido2(self):
        return self._apellido2

    @apellido2.setter
    def apellido2(self, valor):
        self._apellido2 = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = valor

    @property
    def tipo_sangre(self):
        return self._tipo_sangre

    @tipo_sangre.setter
    def tipo_sangre(self, valor):
        self._tipo_sangre = valor

    @property
    def alergias(self):
        return self._alergias

    @alergias.setter
    def alergias(self, valor):
        self._alergias = valor

    @property
    def estado_paciente(self):
        return self._estado_paciente

    @estado_paciente.setter
    def estado_paciente(self, valor):
        self._estado_paciente = valor

    @property
    def calle(self):
        return self._calle

    @property
    def numero(self):
        return self._numero

    @property
    def colonia(self):
        return self._colonia

    @property
    def ciudad(self):
        return self._ciudad

    @property
    def estado(self):
        return self._estado

    @property
    def codigo_postal(self):
        return self._codigo_postal