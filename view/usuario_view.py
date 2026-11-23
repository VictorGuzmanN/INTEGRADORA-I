import tkinter as tk
from tkinter import ttk, messagebox
from controller.auth_controller import AuthController


class UsuarioView:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#F9FAFB")
        self.frame.pack(fill="both", expand=True)
        self.id_seleccionado = None

        tk.Label(self.frame, text="Gestión de usuarios", bg="#F9FAFB", fg="#111827", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(self.frame, text="Administra las cuentas de acceso y privilegios por rol", bg="#F9FAFB", fg="#6B7280", font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 12))

        form = tk.Frame(self.frame, bg="#F3F4F6", padx=18, pady=14)
        form.pack(fill="x", pady=(0, 10))

        tk.Label(form, text="Nombre de Usuario:", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=6, pady=5)
        self.entry_usuario = tk.Entry(form, width=22, bg="#FFFFFF", relief="solid", bd=1)
        self.entry_usuario.grid(row=0, column=1, ipady=3, padx=6, pady=5)

        tk.Label(form, text="Contraseña:", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=6, pady=5)
        self.entry_contrasena = tk.Entry(form, show="*", width=22, bg="#FFFFFF", relief="solid", bd=1)
        self.entry_contrasena.grid(row=0, column=3, ipady=3, padx=6, pady=5)

        tk.Label(form, text="Rol / Campo:", bg="#F3F4F6", fg="#111827", font=("Segoe UI", 9, "bold")).grid(row=0, column=4, sticky="w", padx=6, pady=5)
        self.combo_rol = ttk.Combobox(form, values=["Total", "Doctor", "Paciente"], state="readonly", width=18)
        self.combo_rol.set("Doctor")
        self.combo_rol.grid(row=0, column=5, ipady=2, padx=6, pady=5)

        btns = tk.Frame(self.frame, bg="#F9FAFB")
        btns.pack(fill="x", pady=6)

        tk.Button(btns, text="Registrar usuario", bg="#059669", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.guardar).pack(side="left", padx=(0, 6))
        tk.Button(btns, text="Eliminar usuario", bg="#111827", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=self.eliminar).pack(side="left", padx=6)
        tk.Button(btns, text="Limpiar", bg="#E5E7EB", fg="#1F2937", font=("Segoe UI", 9), relief="flat", padx=14, pady=6, cursor="hand2", command=self.limpiar).pack(side="left", padx=6)

        card_tabla = tk.Frame(self.frame, bg="#F3F4F6", padx=14, pady=12)
        card_tabla.pack(fill="both", expand=True, pady=(6, 0))

        cols = ("ID", "Usuario", "Rol / Privilegios")
        self.tabla = ttk.Treeview(card_tabla, columns=cols, show="headings", height=11)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=200)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.cargar_datos()

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
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        rol = self.combo_rol.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Validación", "Ingrese usuario y contraseña.")
            return

        ok, msg = AuthController.registrar_usuario(usuario, contrasena, rol)
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
        self.combo_rol.set("Doctor")