import reflex as rx
import os
from app import index  # Importa tu página principal desde app.py

# Nombre del proyecto
PROJECT_NAME = "reflex-dashboard"
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

# Agregar la página principal del dashboard
app.add_page(index)

# Opcional: puedes agregar más páginas aquí, ejemplo:
# from otra_pagina import otra
# app.add_page(otra)

# Establece la página de inicio
app.compile()
