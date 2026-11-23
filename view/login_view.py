import tkinter as tk
from tkinter import messagebox, Menu
from controller.auth_controller import AuthController
from view.main_view import MainView
from utils_logo import cargar_logo_tk, aplicar_icono_ventana


class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("SIRCRA - Iniciar sesión")
        self.root.geometry("560x660")
        self.root.configure(bg="#F4F6F8")

        aplicar_icono_ventana(self.root)
        self.logo_login = cargar_logo_tk(74, 82, solo_escudo=True)

        # Asegurar que no quede menú superior visible en el Login
        self.root.config(menu=Menu(self.root))

        for widget in self.root.winfo_children():
            widget.destroy()

        self.correo_recuperacion = ""
        self.usuario_recuperacion = ""
        self.codigo_generado = ""

        self.contenedor = tk.Frame(self.root, bg="#F4F6F8")
        self.contenedor.place(relx=0.5, rely=0.5, anchor="center")

        self.card = tk.Frame(
            self.contenedor,
            bg="#FFFFFF",
            padx=38,
            pady=32,
            highlightbackground="#111827",
            highlightthickness=1
        )
        self.card.pack()

        self.mostrar_login()

    def _limpiar_card(self):
        for widget in self.card.winfo_children():
            widget.destroy()

    def _poner_encabezado_logo(self, subtitulo):
        if self.logo_login:
            lbl_img = tk.Label(self.card, image=self.logo_login, bg="#FFFFFF")
            lbl_img.pack(pady=(0, 6))
        tk.Label(self.card, text="SIRCRA", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 20, "bold")).pack()
        tk.Label(self.card, text=subtitulo, bg="#FFFFFF", fg="#6B7280", font=("Segoe UI", 9)).pack(pady=(2, 14))

    def _crear_entry_con_placeholder(self, parent, placeholder, ocultar=False):
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            width=36,
            relief="solid",
            bd=1,
            fg="#6B7280"
        )
        entry.insert(0, placeholder)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg="#111827", show="*" if ocultar else "")

        def on_focus_out(event):
            if entry.get().strip() == "":
                entry.config(fg="#6B7280", show="")
                entry.insert(0, placeholder)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return entry, placeholder

    def _obtener_valor_entry(self, entry, placeholder):
        val = entry.get().strip()
        return "" if val == placeholder else val

    # ==========================================================
    # PANTALLA 1: INICIAR SESIÓN
    # ==========================================================
    def mostrar_login(self):
        self._limpiar_card()
        self.root.title("SIRCRA - Iniciar sesión")
        self._poner_encabezado_logo("Ingresa tus credenciales para acceder a tu cuenta.")

        tk.Label(self.card, text="Iniciar sesión", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x", pady=(0, 12))

        tk.Label(self.card, text="Usuario", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x")
        self.entry_usuario, self.ph_usuario = self._crear_entry_con_placeholder(self.card, "Ingresa tu usuario")
        self.entry_usuario.pack(fill="x", ipady=7, pady=(4, 14))

        tk.Label(self.card, text="Contraseña", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x")
        self.entry_contrasena, self.ph_contrasena = self._crear_entry_con_placeholder(self.card, "Ingresa tu contraseña", ocultar=True)
        self.entry_contrasena.pack(fill="x", ipady=7, pady=(4, 20))
        self.entry_contrasena.bind("<Return>", lambda e: self.autenticar())

        tk.Button(
            self.card,
            text="Iniciar sesión",
            bg="#009966",
            fg="#FFFFFF",
            activebackground="#007A52",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            pady=10,
            cursor="hand2",
            command=self.autenticar
        ).pack(fill="x")

        tk.Button(
            self.card,
            text="Olvide mi contraseña",
            bg="#FFFFFF",
            fg="#111827",
            activebackground="#FFFFFF",
            activeforeground="#009966",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.mostrar_paso1_recuperar
        ).pack(pady=(14, 0))

    def autenticar(self):
        usuario = self._obtener_valor_entry(self.entry_usuario, self.ph_usuario)
        contrasena = self._obtener_valor_entry(self.entry_contrasena, self.ph_contrasena)

        if not usuario or not contrasena:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa usuario y contraseña.")
            return

        admin = AuthController.iniciar_sesion(usuario, contrasena)
        if admin:
            MainView(self.root, admin)
        else:
            messagebox.showerror("Acceso denegado", "Credenciales incorrectas o sin conexión a MySQL.")

    # ==========================================================
    # PANTALLA 2: RECUPERAR SESIÓN
    # ==========================================================
    def mostrar_paso1_recuperar(self):
        self._limpiar_card()
        self.root.title("SIRCRA - Recuperar sesión")
        self._poner_encabezado_logo("Recuperacion de cuenta")

        tk.Label(self.card, text="Recuperar sesión", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x", pady=(0, 12))

        tk.Label(self.card, text="Correo electrónico", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x")
        entry_correo, ph_correo = self._crear_entry_con_placeholder(self.card, "nombre@correo.com")
        entry_correo.pack(fill="x", ipady=7, pady=(4, 14))

        tk.Label(self.card, text="Nombre de usuario", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x")
        entry_user, ph_user = self._crear_entry_con_placeholder(self.card, "Ingresa tu nombre de usuario")
        entry_user.pack(fill="x", ipady=7, pady=(4, 20))

        def continuar_a_codigo():
            correo = self._obtener_valor_entry(entry_correo, ph_correo)
            usuario = self._obtener_valor_entry(entry_user, ph_user)

            if not correo or not usuario:
                messagebox.showwarning("Campos vacíos", "Ingresa tu correo electrónico y nombre de usuario.")
                return

            ok, msg, codigo = AuthController.solicitar_codigo_recuperacion(correo, usuario)
            if ok:
                self.correo_recuperacion = correo
                self.usuario_recuperacion = usuario
                self.codigo_generado = codigo
                messagebox.showinfo("Código enviado", msg)
                self.mostrar_paso2_codigo()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(
            self.card,
            text="Recuperar",
            bg="#009966",
            fg="#FFFFFF",
            activebackground="#007A52",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            pady=10,
            cursor="hand2",
            command=continuar_a_codigo
        ).pack(fill="x")

        tk.Button(
            self.card,
            text="Volver a iniciar sesión",
            bg="#FFFFFF",
            fg="#6B7280",
            activebackground="#FFFFFF",
            activeforeground="#111827",
            font=("Segoe UI", 9),
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.mostrar_login
        ).pack(pady=(12, 0))

    # ==========================================================
    # PANTALLA 3: CÓDIGO DE VERIFICACIÓN
    # ==========================================================
    def mostrar_paso2_codigo(self):
        self._limpiar_card()
        self.root.title("SIRCRA - Verificar código")
        self._poner_encabezado_logo("Recuperacion de cuenta")

        tk.Label(self.card, text="Recuperar cuenta", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x", pady=(0, 12))

        tk.Label(self.card, text="Codigo de verificacion", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x")
        entry_codigo, ph_codigo = self._crear_entry_con_placeholder(self.card, "Ingresa el código de 6 dígitos")
        entry_codigo.pack(fill="x", ipady=7, pady=(4, 20))

        def verificar_codigo():
            codigo = self._obtener_valor_entry(entry_codigo, ph_codigo)
            if not codigo:
                messagebox.showwarning("Campo vacío", "Ingresa el código de verificación.")
                return
            if codigo == self.codigo_generado:
                self.mostrar_paso3_nueva_contrasena()
            else:
                messagebox.showerror("Código incorrecto", "El código de verificación no coincide.")

        tk.Button(
            self.card,
            text="Recuperar",
            bg="#009966",
            fg="#FFFFFF",
            activebackground="#007A52",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            pady=10,
            cursor="hand2",
            command=verificar_codigo
        ).pack(fill="x")

        tk.Button(
            self.card,
            text="Cancelar",
            bg="#FFFFFF",
            fg="#6B7280",
            activebackground="#FFFFFF",
            activeforeground="#111827",
            font=("Segoe UI", 9),
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.mostrar_login
        ).pack(pady=(12, 0))

    # ==========================================================
    # PANTALLA 4: NUEVA CONTRASEÑA
    # ==========================================================
    def mostrar_paso3_nueva_contrasena(self):
        self._limpiar_card()
        self.root.title("SIRCRA - Nueva contraseña")
        self._poner_encabezado_logo("Ingresa tus nuevas credenciales para acceder a tu cuenta.")

        tk.Label(self.card, text="Iniciar sesión", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x", pady=(0, 12))

        tk.Label(self.card, text="Correo electrónico", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x")
        entry_correo = tk.Entry(self.card, font=("Segoe UI", 10), width=36, relief="solid", bd=1, fg="#111827")
        entry_correo.insert(0, self.correo_recuperacion)
        entry_correo.config(state="readonly")
        entry_correo.pack(fill="x", ipady=7, pady=(4, 14))

        tk.Label(self.card, text="Contraseña Nueva", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x")
        entry_nueva, ph_nueva = self._crear_entry_con_placeholder(self.card, "Ingresa tu nueva contraseña", ocultar=True)
        entry_nueva.pack(fill="x", ipady=7, pady=(4, 20))

        def guardar_datos():
            nueva_pass = self._obtener_valor_entry(entry_nueva, ph_nueva)
            if not nueva_pass:
                messagebox.showwarning("Campo vacío", "Ingresa tu nueva contraseña.")
                return

            ok, msg = AuthController.restablecer_contrasena(self.usuario_recuperacion, nueva_pass)
            if ok:
                messagebox.showinfo("Datos guardados", msg)
                self.mostrar_login()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(
            self.card,
            text="Guardar datos",
            bg="#009966",
            fg="#FFFFFF",
            activebackground="#007A52",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            pady=10,
            cursor="hand2",
            command=guardar_datos
        ).pack(fill="x")