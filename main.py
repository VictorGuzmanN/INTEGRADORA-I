# from admi import Administrador
# from doctores import Doctor
# from pacientes import Paciente
# from tratamiento import Tratamiento

# admin = Administrador("admin", "1234", "Total")

class Inicio(ctk.CTkFrame):
    def __init__(self, master, panel):
        super().__init__(master, fg_color="transparent")
        self.correo = next(c for c, (_, _, n) in USUARIOS_DEMO.items() if n == panel.nombre)
        titulo(self, f"Bienvenido, {panel.nombre}", "Tu perfil en el anexo")
        activos = len(datos.listar(doctor=panel.nombre, estado="Activo"))
        fichas(self, [
            ("Nombre", panel.nombre),
            ("Categoría", datos.ESPECIALIDADES.get(panel.nombre, "Sin categoría")),
            ("Correo", self.correo),
            ("Contraseña", "••••••••"),
            ("Pacientes activos", str(activos)),
        ]).pack(fill="x", padx=22)

        t = tarjeta(self)
        t.pack(fill="x", padx=30, pady=16)
        ctk.CTkLabel(t, text="Cambiar contraseña", text_color=TEXTO,
                     font=("Arial", 16, "bold")).pack(anchor="w", padx=16, pady=(14, 0))
        f, self.w = formulario(t, [("actual", "Contraseña actual", None),
                                   ("nueva", "Nueva contraseña", None),
                                   ("repetir", "Repetir nueva contraseña", None)], columnas=3)
        for w in self.w.values():
            w.configure(show="*")
        f.pack(fill="x", padx=10, pady=6)
        self.msg = ctk.CTkLabel(t, text="")
        self.msg.pack()
        boton(t, "Guardar contraseña", self.guardar).pack(anchor="e", padx=20, pady=(0, 16))

    def guardar(self):
        d = leer(self.w)
        clave, rol, nombre = USUARIOS_DEMO[self.correo]
        if d["actual"] != clave:
            self.msg.configure(text="La contraseña actual es incorrecta", text_color=ROJO)
        elif len(d["nueva"]) < 4:
            self.msg.configure(text="Mínimo 4 caracteres", text_color=ROJO)
        elif d["nueva"] != d["repetir"]:
            self.msg.configure(text="Las contraseñas no coinciden", text_color=ROJO)
        else:
            USUARIOS_DEMO[self.correo] = (d["nueva"], rol, nombre)
            for w in self.w.values():
                w.delete(0, "end")
            self.msg.configure(text="Contraseña actualizada", text_color=VERDE_OSC)


class PanelDoctor(Panel):
    def __init__(self, master, nombre, al_salir):
        super().__init__(master, "doctor", nombre, [("Inicio", Inicio)], al_salir) 

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