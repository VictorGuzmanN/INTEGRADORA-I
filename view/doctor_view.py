import tkinter as tk
from tkinter import ttk, messagebox
from model.doctor import Doctor
from controller.doctor_controller import DoctorController


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
            self.entries[k].insert(0, vals[idx])

    def construir_objeto(self, id_doc=None):
        return Doctor(
            nombre=self.entries["Nombre:"].get().strip(),
            apellido1=self.entries["Apellido Paterno:"].get().strip(),
            apellido2=self.entries["Apellido Materno:"].get().strip(),
            especialidad=self.entries["Especialidad:"].get().strip(),
            numero_cedula=self.entries["Cédula Profesional:"].get().strip(),
            telefono=self.entries["Teléfono:"].get().strip(),
            ciudad=self.entries["Ciudad:"].get().strip(),
            id_doctor=id_doc
        )

    def guardar(self):
        doc = self.construir_objeto()
        if not doc.nombre or not doc.apellido1 or not doc.especialidad or not doc.numero_cedula:
            messagebox.showwarning("Validación", "Complete los campos obligatorios.")
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
        doc = self.construir_objeto(self.id_seleccionado)
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