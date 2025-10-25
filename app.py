import reflex as rx
from state import AuthState, ServerState, TaskState
from rxconfig import app  # Importa el objeto app definido en rxconfig.py


def login_page():
    return rx.center(
        rx.vstack(
            rx.text("🔐 Acceso al Panel", font_size="2xl"),
            rx.input(placeholder="Usuario", on_change=AuthState.set_username),
            rx.input(type_="password", placeholder="Contraseña", on_change=AuthState.set_password),
            rx.button("Iniciar sesión", on_click=AuthState.login),
            rx.text(AuthState.error, color="red"),
        ),
        height="100vh"
    )


def dashboard():
    return rx.vstack(
        rx.hstack(
            rx.button("Cerrar sesión", on_click=AuthState.logout),
            rx.spacer(),
            rx.text("Panel de Control Reflex", font_size="xl")
        ),
        rx.divider(),
        rx.hstack(
            rx.vstack(rx.text("CPU"), rx.text(f"{ServerState.cpu}%")),
            rx.vstack(rx.text("RAM"), rx.text(f"{ServerState.ram}%")),
            rx.vstack(rx.text("Disco"), rx.text(f"{ServerState.disk}%")),
            rx.button("Actualizar", on_click=ServerState.update_metrics),
        ),
        rx.divider(),
        rx.text("🧩 Tareas disponibles", font_size="lg"),
        rx.foreach(
            TaskState.tasks,
            lambda script: rx.hstack(
                rx.text(script),
                rx.button("Ejecutar", on_click=lambda: TaskState.run_task(script)),
                rx.button("Ver log", on_click=lambda: TaskState.view_log(script)),
                rx.button("Programar cada 5 min", on_click=lambda: TaskState.schedule_task(script, 5)),
                rx.button("Detener", on_click=lambda: TaskState.stop_task(script)),
            ),
        ),
        rx.text(TaskState.message, color="green"),
        rx.text_area(TaskState.logs, height="300px", width="100%"),
        padding="2em"
    )


def index():
    return rx.cond(AuthState.logged_in, dashboard(), login_page())


# Registrar la página en el app importado desde rxconfig
app.add_page(index)
