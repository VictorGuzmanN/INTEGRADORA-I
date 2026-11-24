import tkinter as tk
from tkinter import Menu
from view.paciente_view import PacienteView
from view.doctor_view import DoctorView
from view.tratamiento_view import TratamientoView
from view.usuario_view import UsuarioView
from utils_logo import cargar_logo_tk, aplicar_icono_ventana


class MainView(tk.Frame):
    def __init__(self, master, admin):
        super().__init__(master, bg="#F4F6F8")
        self.master = master
        self.admin = admin
        self.rol = self.admin.privilegios.strip().lower()

        self.master.title("SIRCRA - Sistema de Integración de Registros")
        self.master.geometry("1150x680")
        self.master.minsize(980, 600)

        aplicar_icono_ventana(self.master)
        self.logo_header = cargar_logo_tk(38, 42, solo_escudo=True)

        for widget in self.master.winfo_children():
            if widget is not self:
                widget.destroy()

        self.pack(fill="both", expand=True)
        self.botones_nav = {}

        self._construir_header()
        self._construir_cuerpo()
        self.barra_menu()

        if self.rol in ("total", "doctor", "paciente"):
            self.navegar("pacientes", PacienteView)

    def _construir_header(self):
        header = tk.Frame(self, bg="#FFFFFF", height=64, bd=0, highlightthickness=1, highlightbackground="#E0E4E8")
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        # Escudo SIRCRA en el encabezado superior izquierdo
        if self.logo_header:
            lbl_logo = tk.Label(header, image=self.logo_header, bg="#FFFFFF")
            lbl_logo.pack(side="left", padx=(18, 8), pady=8)
        else:
            tk.Label(
                header,
                text="S",
                bg="#0F9D58",
                fg="#FFFFFF",
                font=("Segoe UI", 14, "bold"),
                width=3
            ).pack(side="left", padx=(20, 10), pady=12)

        tk.Label(
            header,
            text="SIRCRA",
            bg="#FFFFFF",
            fg="#111827",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text="Sistema de Integración de Registros para Centros de Rehabilitación de Adicciones",
            bg="#FFFFFF",
            fg="#6B7280",
            font=("Segoe UI", 9)
        ).pack(side="left", padx=(14, 0))

        btn_salir = tk.Button(
            header,
            text="Cerrar sesión",
            bg="#FFFFFF",
            fg="#111827",
            font=("Segoe UI", 9, "bold"),
            relief="solid",
            bd=1,
            padx=14,
            pady=5,
            cursor="hand2",
            command=self.cerrar_sesion
        )
        btn_salir.pack(side="right", padx=20)

        tk.Label(
            header,
            text=f"{self.admin.usuario} ({self.admin.privilegios})",
            bg="#FFFFFF",
            fg="#4B5563",
            font=("Segoe UI", 9)
        ).pack(side="right", padx=(0, 15))

    def _construir_cuerpo(self):
        cuerpo = tk.Frame(self, bg="#F4F6F8")
        cuerpo.pack(side="top", fill="both", expand=True)

        sidebar = tk.Frame(cuerpo, bg="#E5E7EB", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        titulo_rol = {
            "total": "Administrador",
            "doctor": "Doctor",
            "paciente": "Paciente"
        }.get(self.rol, self.admin.privilegios)

        tk.Label(
            sidebar,
            text=titulo_rol,
            bg="#E5E7EB",
            fg="#6B7280",
            font=("Segoe UI", 9, "bold"),
            anchor="w"
        ).pack(fill="x", padx=18, pady=(20, 10))

        if self.rol == "total":
            opciones = [
                ("pacientes", "Gestión de pacientes", PacienteView),
                ("doctores", "Gestión de doctores", DoctorView),
                ("tratamientos", "Tratamientos y diagnósticos", TratamientoView),
                ("usuarios", "Gestión de usuarios", UsuarioView),
            ]
        elif self.rol == "doctor":
            opciones = [
                ("pacientes", "Gestión de pacientes", PacienteView),
                ("tratamientos", "Tratamientos y diagnósticos", TratamientoView),
            ]
        else:
            opciones = [
                ("pacientes", "Mi expediente", PacienteView),
                ("tratamientos", "Mis tratamientos", TratamientoView),
            ]

        for clave, texto, vista_cls in opciones:
            btn = tk.Button(
                sidebar,
                text=texto,
                bg="#E5E7EB",
                fg="#1F2937",
                activebackground="#A7F3D0",
                activeforeground="#065F46",
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                anchor="w",
                padx=18,
                pady=10,
                cursor="hand2",
                command=lambda c=clave, v=vista_cls: self.navegar(c, v)
            )
            btn.pack(fill="x", pady=2)
            self.botones_nav[clave] = btn

        self.content = tk.Frame(cuerpo, bg="#F4F6F8")
        self.content.pack(side="left", fill="both", expand=True, padx=24, pady=20)

    def navegar(self, clave, vista_cls):
        for k, btn in self.botones_nav.items():
            if k == clave:
                btn.config(bg="#A7F3D0", fg="#065F46")
            else:
                btn.config(bg="#E5E7EB", fg="#1F2937")

        for widget in self.content.winfo_children():
            widget.destroy()

        if vista_cls in (PacienteView, TratamientoView):
            vista_cls(self.content, self.admin)
        else:
            vista_cls(self.content)

    # ==========================================================
    # BARRA DE MENÚ SUPERIOR NATIVA
    # ==========================================================
    def barra_menu(self):
        ventana_raiz = self.master.winfo_toplevel()
        menu_bar = Menu(ventana_raiz)
        ventana_raiz.config(menu=menu_bar)

        menu_principal = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Principal", menu=menu_principal)
        menu_principal.add_command(
            label="Pantalla Principal",
            command=lambda: self.navegar("pacientes", PacienteView)
        )
        menu_principal.add_separator()
        menu_principal.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        menu_principal.add_command(label="Salir", command=ventana_raiz.quit)

        menu_modulos = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Módulos", menu=menu_modulos)

        if self.rol == "total":
            menu_modulos.add_command(label="Gestión de pacientes", command=lambda: self.navegar("pacientes", PacienteView))
            menu_modulos.add_command(label="Gestión de doctores", command=lambda: self.navegar("doctores", DoctorView))
            menu_modulos.add_command(label="Tratamientos y diagnósticos", command=lambda: self.navegar("tratamientos", TratamientoView))
            menu_modulos.add_command(label="Gestión de usuarios", command=lambda: self.navegar("usuarios", UsuarioView))
        elif self.rol == "doctor":
            menu_modulos.add_command(label="Gestión de pacientes", command=lambda: self.navegar("pacientes", PacienteView))
            menu_modulos.add_command(label="Tratamientos y diagnósticos", command=lambda: self.navegar("tratamientos", TratamientoView))
        else:
            menu_modulos.add_command(label="Mi expediente", command=lambda: self.navegar("pacientes", PacienteView))
            menu_modulos.add_command(label="Mis tratamientos", command=lambda: self.navegar("tratamientos", TratamientoView))

        if self.rol in ("total", "doctor"):
            menu_acciones = Menu(menu_bar, tearoff=False)
            menu_bar.add_cascade(label="Acciones", menu=menu_acciones)
            menu_acciones.add_command(label="Registrar / Consultar Pacientes", command=lambda: self.navegar("pacientes", PacienteView))
            menu_acciones.add_command(label="Asignar Tratamiento", command=lambda: self.navegar("tratamientos", TratamientoView))
            if self.rol == "total":
                menu_acciones.add_separator()
                menu_acciones.add_command(label="Registrar Doctor", command=lambda: self.navegar("doctores", DoctorView))
                menu_acciones.add_command(label="Administrar Usuarios", command=lambda: self.navegar("usuarios", UsuarioView))

    def cerrar_sesion(self):
        from view.login_view import LoginView

        ventana_raiz = self.master.winfo_toplevel()
        ventana_raiz.config(menu=Menu(ventana_raiz))
        for widget in ventana_raiz.winfo_children():
            widget.destroy()
        LoginView(ventana_raiz)