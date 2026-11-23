import os
import sys
from PIL import Image, ImageTk


def ruta_recurso(ruta_relativa):
    """Obtiene la ruta absoluta del recurso (compatible con PyInstaller .exe y VS Code)."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath("."), ruta_relativa)


def cargar_logo_tk(ancho, alto, solo_escudo=True):
    """Carga el logo de SIRCRA y devuelve un PhotoImage listo para Tkinter."""
    ruta = ruta_recurso(os.path.join("assets", "logo.png"))
    if not os.path.exists(ruta):
        return None
    try:
        img = Image.open(ruta).convert("RGBA")
        if solo_escudo:
            # Recorta el área superior donde está el escudo (quita el texto inferior grande)
            w, h = img.size
            caja = (int(w * 0.28), int(h * 0.04), int(w * 0.72), int(h * 0.65))
            img = img.crop(caja)

        img = img.resize((ancho, alto), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"No se pudo cargar el logo: {e}")
        return None


def aplicar_icono_ventana(ventana):
    """Cambia la pluma de Tkinter por el escudo de SIRCRA en la barra de título."""
    icono = cargar_logo_tk(32, 32, solo_escudo=True)
    if icono:
        ventana.iconphoto(True, icono)
        ventana._icono_sircra_ref = icono  # Evita que Python borre la imagen de memoria