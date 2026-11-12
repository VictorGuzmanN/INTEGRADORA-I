import customtkinter as ctk


class VistaPaciente:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.ventana = ctk.CTk()
        self.ventana.title("Registro de Pacientes")
        self.ventana.geometry("500x500")

        self.titulo = ctk.CTkLabel(
            self.ventana,
            text="REGISTRO DE PACIENTES",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)

        self.entry_nombre = ctk.CTkEntry(
            self.ventana,
            width=300,
            placeholder_text="Nombre"
        )
        self.entry_nombre.pack(pady=10)

        self.entry_telefono = ctk.CTkEntry(
            self.ventana,
            width=300,
            placeholder_text="Teléfono"
        )
        self.entry_telefono.pack(pady=10)

        self.entry_sangre = ctk.CTkEntry(
            self.ventana,
            width=300,
            placeholder_text="Tipo de sangre"
        )
        self.entry_sangre.pack(pady=10)

        self.btn_guardar = ctk.CTkButton(
            self.ventana,
            text="Guardar Paciente"
        )
        self.btn_guardar.pack(pady=20)

        self.txt_resultado = ctk.CTkTextbox(
            self.ventana,
            width=350,
            height=150
        )
        self.txt_resultado.pack(pady=20)

    def obtener_datos(self):

        return (
            self.entry_nombre.get(),
            self.entry_telefono.get(),
            self.entry_sangre.get()
        )

    def mostrar_resultado(self, texto):

        self.txt_resultado.delete("1.0", "end")
        self.txt_resultado.insert("end", texto)

    def iniciar(self):

        self.ventana.mainloop()