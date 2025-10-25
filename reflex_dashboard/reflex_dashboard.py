"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from reflex_dashboard.state import AuthState, ServerState, TaskState, start_log_refresh


class State(rx.State):
    """The app state."""


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
    start_log_refresh()
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
        rx.divider(),
        rx.vstack(
            rx.text(TaskState.message, color="green"),
            rx.text_area(TaskState.logs, height="300px", width="100%"),
            rx.button(
                "Detener actualización de logs",
                on_click=TaskState.stop_auto_update,
                color_scheme="red",
            ),
        ),
        padding="2em"
    )


def index() -> rx.Component:
    return rx.cond(AuthState.logged_in, dashboard(), login_page())
    # Welcome Page (Index)
    # return rx.container(
    #     rx.color_mode.button(position="top-right"),
    #     rx.vstack(
    #         rx.heading("Welcome to Reflex!", size="9"),
    #         rx.text(
    #             "Get started by editing ",
    #             rx.code(f"{config.app_name}/{config.app_name}.py"),
    #             size="5",
    #         ),
    #         rx.link(
    #             rx.button("Check out our docs!"),
    #             href="https://reflex.dev/docs/getting-started/introduction/",
    #             is_external=True,
    #         ),
    #         spacing="5",
    #         justify="center",
    #         min_height="85vh",
    #     ),
    # )


app = rx.App()
app.add_page(index)
