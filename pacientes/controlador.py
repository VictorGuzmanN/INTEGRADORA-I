from pacientes.modelo import Paciente


class ControladorPaciente:

    def __init__(self, vista):

        self.vista = vista

        self.vista.btn_guardar.configure(
            command=self.guardar_paciente
        )

    def guardar_paciente(self):

        nombre, telefono, sangre = self.vista.obtener_datos()

        paciente = Paciente(
            nombre,
            telefono,
            sangre
        )

        self.vista.mostrar_resultado(
            paciente.mostrar_datos()
        )