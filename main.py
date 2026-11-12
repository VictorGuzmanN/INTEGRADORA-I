# from admi import Administrador
# from doctores import Doctor
# from pacientes import Paciente
# from tratamiento import Tratamiento

# admin = Administrador("admin", "1234", "Total")

# doctor = Doctor(
#     "Carlos García",
#     "Psiquiatría",
#     "CED12345"
# )

# paciente = Paciente(
#     "Juan Pérez",
#     "6181234567",
#     "O+"
# )

# tratamiento = Tratamiento(
#     "25/10/2026",
#     "Terapia Conductual",
#     "Dependencia al alcohol"
# )

# admin.mostrar_datos()

# doctor.atender_paciente()
# doctor.generar_diagnostico()
# doctor.asignar_tratamiento()

# paciente.registrarse()
# paciente.consultar_diagnostico()

# tratamiento.registrar_tratamiento()


from pacientes.vista import VistaPaciente
from pacientes.controlador import ControladorPaciente


vista = VistaPaciente()

controlador = ControladorPaciente(vista)

vista.iniciar()