import tkinter as tk
from tkinter import ttk, messagebox
from model.paciente import Paciente
from controller.paciente_controller import PacienteController
from utils_validacion import ValidationError, validar_solo_letras, validar_telefono, validar_tipo_sangre


class PacienteView:
    def __init__(self, parent, admin=None):
        self.frame = tk.Frame(parent, bg="#F9FAFB")
        self.frame.pack(fill="both", expand=True)
        self.admin = admin
        self.rol = self.admin.privilegios.strip().lower() if self.admin else "total"
        self.es_paciente = self.rol == "paciente"
        self.id_seleccionado = None

        titulo = "Mi expediente clínico" if self.es_paciente else "Gestión de pacientes"
        subtitulo = "Consulta tus datos personales y estado clínico actual (solo lectura)" if self.es_paciente else "Consulta y administra los pacientes registrados"

        tk.Label(self.frame, text=titulo, bg="#F9FAFB", fg="#111827", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(self.frame, text=subtitulo, bg="#F9FAFB", fg="#6B7280", font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 12))

        self.entries = {}

        if not self.es_paciente:
            form = tk.Frame(self.frame, bg="#F3F4F6", padx=18, pady=14)
            form.pack(fill="x", pady=(0, 10))

            campos = [
                ("Nombre:", 0, 0), ("Apellido Paterno:", 0, 2), ("Apellido Materno:", 0, 4),
                ("Teléfono:", 1, 0), ("Tipo de Sangre:", 1, 2), ("Alergias:", 1, 4),
                ("Estado Clínico:", 2, 0)
            ]

            for texto, fila, col in campos:
                tk.Label(form, text=texto, bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=fila, column=col, sticky="w", padx=6, pady=5)
                if texto == "Estado Clínico:":
                    widget = ttk.Combobox(form, values=["Registrado", "Diagnosticado", "En_Tratamiento", "En_Seguimiento", "Egresado", "Reingresado"], state="readonly", width=19)
                    widget.set("Registrado")
                else:
                    widget = tk.Entry(form, width=21, bg="#FFFFFF", relief="solid", bd=1)
                widget.grid(row=fila, column=col + 1, ipady=3, padx=6, pady=5)
                self.entries[texto] = widget

            btns = tk.Frame(self.frame, bg="#F9FAFB")
            btns.pack(fill="x", pady=6)

            tk.Button(btns, text="Guardar paciente", bg="#059669", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.guardar).pack(side="left", padx=(0, 6))
            tk.Button(btns, text="Actualizar paciente", bg="#FFFFFF", fg="#059669", font=("Segoe UI", 9, "bold"), relief="solid", bd=1, padx=14, pady=5, cursor="hand2", command=self.actualizar).pack(side="left", padx=6)
            tk.Button(btns, text="Eliminar paciente", bg="#111827", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.eliminar).pack(side="left", padx=6)
            tk.Button(btns, text="Limpiar", bg="#E5E7EB", fg="#1F2937", font=("Segoe UI", 9), relief="flat", padx=14, pady=6, cursor="hand2", command=self.limpiar).pack(side="left", padx=6)

        card_tabla = tk.Frame(self.frame, bg="#F3F4F6", padx=14, pady=12)
        card_tabla.pack(fill="both", expand=True, pady=(6, 0))

        cols = ("ID", "Nombre", "Apellido1", "Apellido2", "Teléfono", "Sangre", "Alergias", "Estado")
        self.tabla = ttk.Treeview(card_tabla, columns=cols, show="headings", height=10)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=100)
        self.tabla.pack(fill="both", expand=True)

        if not self.es_paciente:
            self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        usuario_actual = self.admin.usuario.strip().lower() if self.admin else ""
        for p in PacienteController.obtener_pacientes():
            if self.es_paciente and p["nombre"].strip().lower() != usuario_actual:
                continue

            self.tabla.insert("", "end", values=(
                p["id_paciente"], p["nombre"], p["apellido1"], p["apellido2"],
                p["telefono"], p["tipo_sangre"], p["alergias"], p["estado_paciente"]
            ))

    def seleccionar_fila(self, event):
        if self.es_paciente:
            return
        sel = self.tabla.selection()
        if not sel:
            return
        vals = self.tabla.item(sel[0])["values"]
        self.id_seleccionado = vals[0]
        campos_texto = [
            ("Nombre:", 1), ("Apellido Paterno:", 2), ("Apellido Materno:", 3),
            ("Teléfono:", 4), ("Tipo de Sangre:", 5), ("Alergias:", 6)
        ]
        for clave, idx in campos_texto:
            self.entries[clave].delete(0, tk.END)
            val = "" if str(vals[idx]) == "None" else vals[idx]
            self.entries[clave].insert(0, val)
        self.entries["Estado Clínico:"].set(vals[7])

    def validar_y_construir(self, id_pac=None):
        nombre = validar_solo_letras(self.entries["Nombre:"].get(), "Nombre", obligatorio=True)
        apellido1 = validar_solo_letras(self.entries["Apellido Paterno:"].get(), "Apellido Paterno", obligatorio=True)
        apellido2 = validar_solo_letras(self.entries["Apellido Materno:"].get(), "Apellido Materno", obligatorio=False)
        telefono = validar_telefono(self.entries["Teléfono:"].get(), "Teléfono", obligatorio=True)
        tipo_sangre = validar_tipo_sangre(self.entries["Tipo de Sangre:"].get())
        alergias = validar_solo_letras(self.entries["Alergias:"].get(), "Alergias", obligatorio=False) or "Ninguna"

        return Paciente(
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            telefono=telefono,
            tipo_sangre=tipo_sangre,
            alergias=alergias,
            estado_paciente=self.entries["Estado Clínico:"].get(),
            id_paciente=id_pac
        )

    def guardar(self):
        if self.es_paciente:
            return
        try:
            pac = self.validar_y_construir()
        except ValidationError as e:
            messagebox.showwarning("Error de validación", str(e))
            return

        ok, msg = PacienteController.registrar_paciente(pac)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar()
            self.cargar_datos()
        else:
            messagebox.showerror("Error", msg)

    def actualizar(self):
        if self.es_paciente:
            return
        if not self.id_seleccionado:
            messagebox.showwarning("Selección", "Seleccione un paciente de la tabla.")
            return
        try:
            pac = self.validar_y_construir(self.id_seleccionado)
        except ValidationError as e:
            messagebox.showwarning("Error de validación", str(e))
            return

        ok, msg = PacienteController.actualizar_paciente(pac)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar()
            self.cargar_datos()
        else:
            messagebox.showerror("Error", msg)

    def eliminar(self):
        if self.es_paciente:
            return
        if not self.id_seleccionado:
            messagebox.showwarning("Selección", "Seleccione un paciente de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el expediente seleccionado?"):
            ok, msg = PacienteController.eliminar_paciente(self.id_seleccionado)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.limpiar()
                self.cargar_datos()
            else:
                messagebox.showerror("Error", msg)

    def limpiar(self):
        if self.es_paciente:
            return
        self.id_seleccionado = None
        for k, w in self.entries.items():
            if k == "Estado Clínico:":
                w.set("Registrado")
            else:
                w.delete(0, tk.END)