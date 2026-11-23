import os
import mysql.connector
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()


class ConexionBD:
    @staticmethod
    def obtener_conexion():
        try:
            conexion = mysql.connector.connect(
                host=os.getenv("DB_HOST", "127.0.0.1"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "sircra_db"),
                use_pure=True
            )
            return conexion
        except Exception as e:
            messagebox.showerror("Error de conexión MySQL", f"No se pudo conectar a la base de datos:\n{e}")
            return None