class Tratamiento:
    def __init__(self, id_doctor, id_paciente, fecha, hora, tratamiento,
                 diagnostico_inicial, fecha_entrada, id_tratamiento=None):
        self._id_tratamiento = id_tratamiento
        self._id_doctor = id_doctor
        self._id_paciente = id_paciente
        self._fecha = fecha
        self._hora = hora
        self._tratamiento = tratamiento
        self._diagnostico_inicial = diagnostico_inicial
        self._fecha_entrada = fecha_entrada

    @property
    def id_tratamiento(self):
        return self._id_tratamiento

    @property
    def id_doctor(self):
        return self._id_doctor

    @id_doctor.setter
    def id_doctor(self, valor):
        self._id_doctor = valor

    @property
    def id_paciente(self):
        return self._id_paciente

    @id_paciente.setter
    def id_paciente(self, valor):
        self._id_paciente = valor

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor

    @property
    def hora(self):
        return self._hora

    @hora.setter
    def hora(self, valor):
        self._hora = valor

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

    @property
    def fecha_entrada(self):
        return self._fecha_entrada

    @fecha_entrada.setter
    def fecha_entrada(self, valor):
        self._fecha_entrada = valor