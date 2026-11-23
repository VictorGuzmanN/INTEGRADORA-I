class Doctor:
    def __init__(self, nombre, apellido1, apellido2, especialidad, numero_cedula,
                 telefono="", calle="", numero="", colonia="", ciudad="", estado="",
                 codigo_postal="", id_doctor=None):
        self._id_doctor = id_doctor
        self._nombre = nombre
        self._apellido1 = apellido1
        self._apellido2 = apellido2
        self._especialidad = especialidad
        self._numero_cedula = numero_cedula
        self._telefono = telefono
        self._calle = calle
        self._numero = numero
        self._colonia = colonia
        self._ciudad = ciudad
        self._estado = estado
        self._codigo_postal = codigo_postal

    @property
    def id_doctor(self):
        return self._id_doctor

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

    @property
    def telefono(self):
        return self._telefono

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