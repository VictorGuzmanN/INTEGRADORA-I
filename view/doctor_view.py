import tkinter as tk
from tkinter import ttk, messagebox
from model.doctor import Doctor
from controller.doctor_controller import DoctorController
from utils_validacion import ValidationError, validar_solo_letras, validar_telefono, validar_alfanumerico


class DoctorView:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#F9FAFB")
        self.frame.pack(fill="both", expand=True)
        self.id_seleccionado = None

        tk.Label(self.frame, text="Gestión de doctores", bg="#F9FAFB", fg="#111827", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(self.frame, text="Consulta y administra el personal médico registrado", bg="#F9FAFB", fg="#6B7280", font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 12))

        form = tk.Frame(self.frame, bg="#F3F4F6", padx=18, pady=14)
        form.pack(fill="x", pady=(0, 10))

        campos = [
            ("Nombre:", 0, 0), ("Apellido Paterno:", 0, 2), ("Apellido Materno:", 0, 4),
            ("Especialidad:", 1, 0), ("Cédula Profesional:", 1, 2), ("Teléfono:", 1, 4),
            ("Ciudad:", 2, 0)
        ]
        self.entries = {}

        for texto, fila, col in campos:
            tk.Label(form, text=texto, bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=fila, column=col, sticky="w", padx=6, pady=5)
            ent = tk.Entry(form, width=21, bg="#FFFFFF", relief="solid", bd=1)
            ent.grid(row=fila, column=col + 1, ipady=3, padx=6, pady=5)
            self.entries[texto] = ent

        btns = tk.Frame(self.frame, bg="#F9FAFB")
        btns.pack(fill="x", pady=6)

        tk.Button(btns, text="Guardar doctor", bg="#059669", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.guardar).pack(side="left", padx=(0, 6))
        tk.Button(btns, text="Actualizar doctor", bg="#FFFFFF", fg="#059669", font=("Segoe UI", 9, "bold"), relief="solid", bd=1, padx=14, pady=5, cursor="hand2", command=self.actualizar).pack(side="left", padx=6)
        tk.Button(btns, text="Eliminar doctor", bg="#111827", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.eliminar).pack(side="left", padx=6)
        tk.Button(btns, text="Limpiar", bg="#E5E7EB", fg="#1F2937", font=("Segoe UI", 9), relief="flat", padx=14, pady=6, cursor="hand2", command=self.limpiar).pack(side="left", padx=6)

        card_tabla = tk.Frame(self.frame, bg="#F3F4F6", padx=14, pady=12)
        card_tabla.pack(fill="both", expand=True, pady=(6, 0))

        cols = ("ID", "Nombre", "Apellido1", "Apellido2", "Especialidad", "Cédula", "Teléfono", "Ciudad")
        self.tabla = ttk.Treeview(card_tabla, columns=cols, show="headings", height=10)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=100)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for d in DoctorController.obtener_doctores():
            self.tabla.insert("", "end", values=(
                d["id_doctor"], d["nombre"], d["apellido1"], d["apellido2"],
                d["especialidad"], d["numero_cedula"], d["telefono"], d["ciudad"]
            ))

    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        vals = self.tabla.item(sel[0])["values"]
        self.id_seleccionado = vals[0]
        keys = ["Nombre:", "Apellido Paterno:", "Apellido Materno:", "Especialidad:", "Cédula Profesional:", "Teléfono:", "Ciudad:"]
        for idx, k in enumerate(keys, 1):
            self.entries[k].delete(0, tk.END)
            val = "" if str(vals[idx]) == "None" else vals[idx]
            self.entries[k].insert(0, val)

    def validar_y_construir(self, id_doc=None):
        nombre = validar_solo_letras(self.entries["Nombre:"].get(), "Nombre", obligatorio=True)
        apellido1 = validar_solo_letras(self.entries["Apellido Paterno:"].get(), "Apellido Paterno", obligatorio=True)
        apellido2 = validar_solo_letras(self.entries["Apellido Materno:"].get(), "Apellido Materno", obligatorio=False)
        especialidad = validar_solo_letras(self.entries["Especialidad:"].get(), "Especialidad", obligatorio=True)
        cedula = validar_alfanumerico(self.entries["Cédula Profesional:"].get(), "Cédula Profesional", obligatorio=True)
        telefono = validar_telefono(self.entries["Teléfono:"].get(), "Teléfono", obligatorio=True)
        ciudad = validar_solo_letras(self.entries["Ciudad:"].get(), "Ciudad", obligatorio=True)

        return Doctor(
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            especialidad=especialidad,
            numero_cedula=cedula,
            telefono=telefono,
            ciudad=ciudad,
            id_doctor=id_doc
        )

    def guardar(self):
        try:
            doc = self.validar_y_construir()
        except ValidationError as e:
            messagebox.showwarning("Error de validación", str(e))
            return

        ok, msg = DoctorController.registrar_doctor(doc)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar()
            self.cargar_datos()
        else:
            messagebox.showerror("Error", msg)

    def actualizar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Selección", "Seleccione un doctor de la tabla.")
            return
        try:
            doc = self.validar_y_construir(self.id_seleccionado)
        except ValidationError as e:
            messagebox.showwarning("Error de validación", str(e))
            return

        ok, msg = DoctorController.actualizar_doctor(doc)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar()
            self.cargar_datos()
        else:
            messagebox.showerror("Error", msg)

    def eliminar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Selección", "Seleccione un doctor de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar al doctor seleccionado?"):
            ok, msg = DoctorController.eliminar_doctor(self.id_seleccionado)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.limpiar()
                self.cargar_datos()
            else:
                messagebox.showerror("Error", msg)

    def limpiar(self):
        self.id_seleccionado = None
        for w in self.entries.values():
            w.delete(0, tk.END)