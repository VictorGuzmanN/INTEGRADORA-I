import tkinter as tk
from tkinter import ttk, messagebox
from controller.auth_controller import AuthController
from utils_validacion import (
    ValidationError,
    validar_solo_letras,
    validar_telefono,
    validar_alfanumerico,
    validar_tipo_sangre
)


class UsuarioView:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#F9FAFB")
        self.frame.pack(fill="both", expand=True)
        self.id_seleccionado = None
        self.entries_extra = {}

        tk.Label(self.frame, text="Gestión de usuarios", bg="#F9FAFB", fg="#111827", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(self.frame, text="Selecciona primero el rol para completar los datos requeridos del perfil", bg="#F9FAFB", fg="#6B7280", font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 12))

        # Paso 1: Selección de Rol y Credenciales
        form_base = tk.Frame(self.frame, bg="#F3F4F6", padx=18, pady=14)
        form_base.pack(fill="x", pady=(0, 8))

        tk.Label(form_base, text="1. Tipo de Rol:", bg="#F3F4F6", fg="#065F46", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=6, pady=5)
        self.combo_rol = ttk.Combobox(form_base, values=["Total", "Doctor", "Paciente"], state="readonly", width=20)
        self.combo_rol.set("Seleccione un rol...")
        self.combo_rol.grid(row=0, column=1, ipady=2, padx=6, pady=5)
        self.combo_rol.bind("<<ComboboxSelected>>", self.on_rol_cambiado)

        tk.Label(form_base, text="Nombre de Usuario:", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=6, pady=5)
        self.entry_usuario = tk.Entry(form_base, width=22, bg="#FFFFFF", relief="solid", bd=1)
        self.entry_usuario.grid(row=0, column=3, ipady=3, padx=6, pady=5)

        tk.Label(form_base, text="Contraseña:", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=0, column=4, sticky="w", padx=6, pady=5)
        self.entry_contrasena = tk.Entry(form_base, show="*", width=22, bg="#FFFFFF", relief="solid", bd=1)
        self.entry_contrasena.grid(row=0, column=5, ipady=3, padx=6, pady=5)

        # Paso 2: Contenedor dinámico para campos según el rol
        self.form_dinamico = tk.Frame(self.frame, bg="#ECFDF5", padx=18, pady=12, highlightbackground="#A7F3D0", highlightthickness=1)

        btns = tk.Frame(self.frame, bg="#F9FAFB")
        btns.pack(fill="x", pady=6)

        tk.Button(btns, text="Registrar usuario", bg="#059669", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.guardar).pack(side="left", padx=(0, 6))
        tk.Button(btns, text="Eliminar usuario", bg="#111827", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.eliminar).pack(side="left", padx=6)
        tk.Button(btns, text="Limpiar", bg="#E5E7EB", fg="#1F2937", font=("Segoe UI", 9), relief="flat", padx=14, pady=6, cursor="hand2", command=self.limpiar).pack(side="left", padx=6)
        self.btns_frame = btns

        card_tabla = tk.Frame(self.frame, bg="#F3F4F6", padx=14, pady=12)
        card_tabla.pack(fill="both", expand=True, pady=(6, 0))

        cols = ("ID", "Usuario", "Rol / Privilegios")
        self.tabla = ttk.Treeview(card_tabla, columns=cols, show="headings", height=10)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=200)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.cargar_datos()

    def on_rol_cambiado(self, event=None):
        for w in self.form_dinamico.winfo_children():
            w.destroy()
        self.entries_extra.clear()

        rol = self.combo_rol.get()
        if rol not in ("Doctor", "Paciente"):
            self.form_dinamico.pack_forget()
            return

        self.form_dinamico.pack(fill="x", pady=(0, 8), before=self.btns_frame)

        if rol == "Doctor":
            tk.Label(self.form_dinamico, text="2. Datos del Doctor (obligatorios para su expediente médico):", bg="#ECFDF5", fg="#065F46", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, columnspan=6, sticky="w", padx=6, pady=(0, 6))
            campos = [
                ("nombre", "Nombre:*", 1, 0), ("apellido1", "Apellido Paterno:*", 1, 2), ("apellido2", "Apellido Materno:", 1, 4),
                ("especialidad", "Especialidad:*", 2, 0), ("numero_cedula", "Cédula Profesional:*", 2, 2), ("telefono", "Teléfono:*", 2, 4),
                ("ciudad", "Ciudad:*", 3, 0)
            ]
            for clave, etiqueta, fila, col in campos:
                tk.Label(self.form_dinamico, text=etiqueta, bg="#ECFDF5", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=fila, column=col, sticky="w", padx=6, pady=4)
                ent = tk.Entry(self.form_dinamico, width=21, bg="#FFFFFF", relief="solid", bd=1)
                ent.grid(row=fila, column=col + 1, ipady=3, padx=6, pady=4)
                self.entries_extra[clave] = ent

        elif rol == "Paciente":
            tk.Label(self.form_dinamico, text="2. Datos del Paciente (obligatorios para su expediente clínico):", bg="#ECFDF5", fg="#065F46", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, columnspan=6, sticky="w", padx=6, pady=(0, 6))
            campos = [
                ("nombre", "Nombre:*", 1, 0), ("apellido1", "Apellido Paterno:*", 1, 2), ("apellido2", "Apellido Materno:", 1, 4),
                ("telefono", "Teléfono:*", 2, 0), ("tipo_sangre", "Tipo de Sangre:*", 2, 2), ("alergias", "Alergias:", 2, 4),
                ("estado_paciente", "Estado Clínico:", 3, 0)
            ]
            for clave, etiqueta, fila, col in campos:
                tk.Label(self.form_dinamico, text=etiqueta, bg="#ECFDF5", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=fila, column=col, sticky="w", padx=6, pady=4)
                if clave == "estado_paciente":
                    widget = ttk.Combobox(self.form_dinamico, values=["Registrado", "Diagnosticado", "En_Tratamiento", "En_Seguimiento", "Egresado", "Reingresado"], state="readonly", width=19)
                    widget.set("Registrado")
                else:
                    widget = tk.Entry(self.form_dinamico, width=21, bg="#FFFFFF", relief="solid", bd=1)
                widget.grid(row=fila, column=col + 1, ipady=3, padx=6, pady=4)
                self.entries_extra[clave] = widget

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for u in AuthController.obtener_usuarios():
            self.tabla.insert("", "end", values=(u["id_admin"], u["usuario"], u["privilegios"]))

    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        vals = self.tabla.item(sel[0])["values"]
        self.id_seleccionado = vals[0]

    def guardar(self):
        rol = self.combo_rol.get()
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if rol not in ("Total", "Doctor", "Paciente"):
            messagebox.showwarning("Rol requerido", "Primero selecciona qué tipo de rol llevará el usuario (Total, Doctor o Paciente).")
            return

        if not usuario or not contrasena:
            messagebox.showwarning("Validación", "Ingrese nombre de usuario y contraseña.")
            return

        datos_extra = {}
        try:
            if rol == "Doctor":
                datos_extra = {
                    "nombre": validar_solo_letras(self.entries_extra["nombre"].get(), "Nombre", obligatorio=True),
                    "apellido1": validar_solo_letras(self.entries_extra["apellido1"].get(), "Apellido Paterno", obligatorio=True),
                    "apellido2": validar_solo_letras(self.entries_extra["apellido2"].get(), "Apellido Materno", obligatorio=False),
                    "especialidad": validar_solo_letras(self.entries_extra["especialidad"].get(), "Especialidad", obligatorio=True),
                    "numero_cedula": validar_alfanumerico(self.entries_extra["numero_cedula"].get(), "Cédula Profesional", obligatorio=True),
                    "telefono": validar_telefono(self.entries_extra["telefono"].get(), "Teléfono", obligatorio=True),
                    "ciudad": validar_solo_letras(self.entries_extra["ciudad"].get(), "Ciudad", obligatorio=True),
                }
            elif rol == "Paciente":
                datos_extra = {
                    "nombre": validar_solo_letras(self.entries_extra["nombre"].get(), "Nombre", obligatorio=True),
                    "apellido1": validar_solo_letras(self.entries_extra["apellido1"].get(), "Apellido Paterno", obligatorio=True),
                    "apellido2": validar_solo_letras(self.entries_extra["apellido2"].get(), "Apellido Materno", obligatorio=False),
                    "telefono": validar_telefono(self.entries_extra["telefono"].get(), "Teléfono", obligatorio=True),
                    "tipo_sangre": validar_tipo_sangre(self.entries_extra["tipo_sangre"].get()),
                    "alergias": validar_solo_letras(self.entries_extra["alergias"].get(), "Alergias", obligatorio=False) or "Ninguna",
                    "estado_paciente": self.entries_extra["estado_paciente"].get(),
                }
        except ValidationError as e:
            messagebox.showwarning("Error de validación", str(e))
            return

        ok, msg = AuthController.registrar_usuario(usuario, contrasena, rol, datos_extra)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar()
            self.cargar_datos()
        else:
            messagebox.showerror("Error", msg)

    def eliminar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Selección", "Seleccione un usuario de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el usuario seleccionado?"):
            ok, msg = AuthController.eliminar_usuario(self.id_seleccionado)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.limpiar()
                self.cargar_datos()
            else:
                messagebox.showerror("Error", msg)

    def limpiar(self):
        self.id_seleccionado = None
        self.entry_usuario.delete(0, tk.END)
        self.entry_contrasena.delete(0, tk.END)
        self.combo_rol.set("Seleccione un rol...")
        self.on_rol_cambiado()