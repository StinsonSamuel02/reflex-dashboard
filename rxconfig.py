import reflex as rx
import os

# Nombre del proyecto
PROJECT_NAME = "reflex_dashboard"
PROJECT_VERSION = "1.0.0"

# Carpeta donde se genera el build de frontend
BUILD_DIR = ".web"

# Configuración principal de la app Reflex
app = rx.App(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
    frontend_build_dir=BUILD_DIR,
    env=os.environ.get("REFLEX_ENV", "prod")  # Usa REFLEX_ENV=prod si está definido
)

# NO importar app.py aquí para evitar import circular
# Las páginas se agregan desde app.py con app.add_page(index)
