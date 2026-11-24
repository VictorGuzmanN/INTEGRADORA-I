import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from model.tratamiento import Tratamiento
from controller.tratamiento_controller import TratamientoController
from controller.doctor_controller import DoctorController
from controller.paciente_controller import PacienteController
from utils_validacion import ValidationError, validar_fecha, validar_hora


class TratamientoView:
    def __init__(self, parent, admin=None):
        self.frame = tk.Frame(parent, bg="#F9FAFB")
        self.frame.pack(fill="both", expand=True)
        self.admin = admin
        self.rol = self.admin.privilegios.strip().lower() if self.admin else "total"
        self.es_paciente = self.rol == "paciente"
        self.id_seleccionado = None
        self.mapa_doctores = {}
        self.mapa_pacientes = {}

        titulo = "Mis tratamientos y diagnósticos" if self.es_paciente else "Tratamientos y diagnósticos"
        subtitulo = "Consulta las terapias y diagnósticos asignados por tu médico (solo lectura)" if self.es_paciente else "Asigna terapias y diagnósticos clínicos a los pacientes"

        tk.Label(self.frame, text=titulo, bg="#F9FAFB", fg="#111827", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(self.frame, text=subtitulo, bg="#F9FAFB", fg="#6B7280", font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 12))

        if not self.es_paciente:
            form = tk.Frame(self.frame, bg="#F3F4F6", padx=18, pady=14)
            form.pack(fill="x", pady=(0, 10))

            tk.Label(form, text="Doctor:", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=6, pady=5)
            self.combo_doctor = ttk.Combobox(form, state="readonly", width=26)
            self.combo_doctor.grid(row=0, column=1, ipady=2, padx=6, pady=5)

            tk.Label(form, text="Paciente:", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=6, pady=5)
            self.combo_paciente = ttk.Combobox(form, state="readonly", width=26)
            self.combo_paciente.grid(row=0, column=3, ipady=2, padx=6, pady=5)

            tk.Label(form, text="Fecha (AAAA-MM-DD):", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=6, pady=5)
            self.entry_fecha = tk.Entry(form, width=28, bg="#FFFFFF", relief="solid", bd=1)
            self.entry_fecha.insert(0, str(date.today()))
            self.entry_fecha.grid(row=1, column=1, ipady=3, padx=6, pady=5)

            tk.Label(form, text="Hora (HH:MM):", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="w", padx=6, pady=5)
            self.entry_hora = tk.Entry(form, width=28, bg="#FFFFFF", relief="solid", bd=1)
            self.entry_hora.insert(0, "10:00")
            self.entry_hora.grid(row=1, column=3, ipady=3, padx=6, pady=5)

            tk.Label(form, text="Tratamiento:", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=6, pady=5)
            self.entry_tratamiento = tk.Entry(form, width=28, bg="#FFFFFF", relief="solid", bd=1)
            self.entry_tratamiento.grid(row=2, column=1, ipady=3, padx=6, pady=5)

            tk.Label(form, text="Diagnóstico Inicial:", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=2, column=2, sticky="w", padx=6, pady=5)
            self.entry_diagnostico = tk.Entry(form, width=28, bg="#FFFFFF", relief="solid", bd=1)
            self.entry_diagnostico.grid(row=2, column=3, ipady=3, padx=6, pady=5)

            tk.Label(form, text="Fecha Entrada:", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", padx=6, pady=5)
            self.entry_entrada = tk.Entry(form, width=28, bg="#FFFFFF", relief="solid", bd=1)
            self.entry_entrada.insert(0, str(date.today()))
            self.entry_entrada.grid(row=3, column=1, ipady=3, padx=6, pady=5)

            btns = tk.Frame(self.frame, bg="#F9FAFB")
            btns.pack(fill="x", pady=6)

            tk.Button(btns, text="Guardar tratamiento", bg="#059669", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.guardar).pack(side="left", padx=(0, 6))
            tk.Button(btns, text="Actualizar", bg="#FFFFFF", fg="#059669", font=("Segoe UI", 9, "bold"), relief="solid", bd=1, padx=14, pady=5, cursor="hand2", command=self.actualizar).pack(side="left", padx=6)
            tk.Button(btns, text="Eliminar", bg="#111827", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.eliminar).pack(side="left", padx=6)
            tk.Button(btns, text="Recargar listas", bg="#A7F3D0", fg="#065F46", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.recargar_combos).pack(side="left", padx=6)
            tk.Button(btns, text="Limpiar", bg="#E5E7EB", fg="#1F2937", font=("Segoe UI", 9), relief="flat", padx=14, pady=6, cursor="hand2", command=self.limpiar).pack(side="left", padx=6)

            self.recargar_combos()

        card_tabla = tk.Frame(self.frame, bg="#F3F4F6", padx=14, pady=12)
        card_tabla.pack(fill="both", expand=True, pady=(6, 0))

        cols = ("ID", "Doctor", "Paciente", "Fecha", "Hora", "Tratamiento", "Diagnóstico", "Entrada")
        self.tabla = ttk.Treeview(card_tabla, columns=cols, show="headings", height=9)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=100)
        self.tabla.pack(fill="both", expand=True)

        if not self.es_paciente:
            self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.cargar_datos()

    def recargar_combos(self):
        if self.es_paciente:
            return
        self.mapa_doctores.clear()
        for d in DoctorController.obtener_doctores():
            etiqueta = f"{d['id_doctor']} - {d['nombre']} {d['apellido1']}"
            self.mapa_doctores[etiqueta] = d["id_doctor"]
        self.combo_doctor["values"] = list(self.mapa_doctores.keys())

        self.mapa_pacientes.clear()
        for p in PacienteController.obtener_pacientes():
            etiqueta = f"{p['id_paciente']} - {p['nombre']} {p['apellido1']}"
            self.mapa_pacientes[etiqueta] = p["id_paciente"]
        self.combo_paciente["values"] = list(self.mapa_pacientes.keys())

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        usuario_actual = self.admin.usuario.strip().lower() if self.admin else ""
        for t in TratamientoController.obtener_tratamientos():
            if self.es_paciente and not t["paciente"].strip().lower().startswith(usuario_actual):
                continue

            self.tabla.insert("", "end", values=(
                t["id_tratamiento"], f"{t['id_doctor']} - {t['doctor']}",
                f"{t['id_paciente']} - {t['paciente']}", str(t["fecha"]),
                str(t["hora"])[:5], t["tratamiento"], t["diagnostico_inicial"], str(t["fecha_entrada"])
            ))

    def seleccionar_fila(self, event):
        if self.es_paciente:
            return
        sel = self.tabla.selection()
        if not sel:
            return
        vals = self.tabla.item(sel[0])["values"]
        self.id_seleccionado = vals[0]
        self.combo_doctor.set(vals[1])
        self.combo_paciente.set(vals[2])
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, vals[3])
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, str(vals[4])[:5])
        self.entry_tratamiento.delete(0, tk.END)
        self.entry_tratamiento.insert(0, vals[5])
        self.entry_diagnostico.delete(0, tk.END)
        self.entry_diagnostico.insert(0, vals[6])
        self.entry_entrada.delete(0, tk.END)
        self.entry_entrada.insert(0, vals[7])

    def validar_y_construir(self, id_trat=None):
        doc_key = self.combo_doctor.get()
        pac_key = self.combo_paciente.get()
        if doc_key not in self.mapa_doctores or pac_key not in self.mapa_pacientes:
            raise ValidationError("Debe seleccionar un Doctor y un Paciente de las listas.")

        fecha = validar_fecha(self.entry_fecha.get(), "Fecha")
        hora = validar_hora(self.entry_hora.get(), "Hora")
        tratamiento = self.entry_tratamiento.get().strip()
        diagnostico = self.entry_diagnostico.get().strip()
        if not tratamiento or not diagnostico:
            raise ValidationError("Los campos 'Tratamiento' y 'Diagnóstico Inicial' son obligatorios.")
        fecha_entrada = validar_fecha(self.entry_entrada.get(), "Fecha Entrada")

        return Tratamiento(
            id_doctor=self.mapa_doctores[doc_key],
            id_paciente=self.mapa_pacientes[pac_key],
            fecha=fecha,
            hora=hora,
            tratamiento=tratamiento,
            diagnostico_inicial=diagnostico,
            fecha_entrada=fecha_entrada,
            id_tratamiento=id_trat
        )

    def guardar(self):
        if self.es_paciente:
            return
        try:
            trat = self.validar_y_construir()
        except ValidationError as e:
            messagebox.showwarning("Error de validación", str(e))
            return

        ok, msg = TratamientoController.registrar_tratamiento(trat)
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
            messagebox.showwarning("Selección", "Seleccione un tratamiento de la tabla.")
            return
        try:
            trat = self.validar_y_construir(self.id_seleccionado)
        except ValidationError as e:
            messagebox.showwarning("Error de validación", str(e))
            return

        ok, msg = TratamientoController.actualizar_tratamiento(trat)
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
            messagebox.showwarning("Selección", "Seleccione un tratamiento de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el tratamiento seleccionado?"):
            ok, msg = TratamientoController.eliminar_tratamiento(self.id_seleccionado)
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
        self.combo_doctor.set("")
        self.combo_paciente.set("")
        self.entry_tratamiento.delete(0, tk.END)
        self.entry_diagnostico.delete(0, tk.END)