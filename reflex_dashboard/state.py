import reflex as rx
import psutil
import subprocess
import os
import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

scheduler = BackgroundScheduler()
scheduler.start()

USERS = {"admin": "admin123"}


class AuthState(rx.State):
    logged_in: bool = False
    username: str = ""
    password: str = ""
    error: str = ""

    def login(self):
        if USERS.get(self.username) == self.password:
            self.logged_in = True
            self.error = ""
        else:
            self.error = "Credenciales inválidas"

    def logout(self):
        self.logged_in = False
        self.username = ""
        self.password = ""


class ServerState(rx.State):
    cpu: float = 0.0
    ram: float = 0.0
    disk: float = 0.0

    def update_metrics(self):
        self.cpu = psutil.cpu_percent(interval=0.5)
        self.ram = psutil.virtual_memory().percent
        self.disk = psutil.disk_usage("/").percent


class TaskState(rx.State):
    """Estado para manejar las tareas y logs."""
    TASKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tasks"))
    tasks: list[str] = os.listdir(TASKS_DIR) if os.path.exists(TASKS_DIR) else []

    message: str = ""
    logs: str = ""
    current_script: str = ""  # script actualmente mostrado
    auto_update: bool = False  # controla si se debe actualizar en tiempo real

    def run_task(self, script: str):
        """Ejecuta una tarea y comienza a mostrar su log."""
        log_file = f"logs/{script.replace('.py', '')}.log"
        script_path = os.path.join(self.TASKS_DIR, script)
        try:
            subprocess.Popen(
                ["python3", script_path],
                stdout=open(log_file, "a"),
                stderr=open(log_file, "a"),
            )
            self.message = f"Tarea '{script}' lanzada correctamente."
            self.current_script = script
            self.auto_update = True
            self._load_log(script)
        except Exception as e:
            self.message = f"Error ejecutando tarea: {e}"
        return self

    def view_log(self, script: str):
        """Muestra y activa la actualización automática del log del script dado."""
        self.current_script = script
        self.auto_update = True
        self._load_log(script)
        return self

    def stop_auto_update(self):
        """Detiene la actualización automática del log."""
        self.auto_update = False
        self.message = "Actualización automática detenida."
        return self

    def _load_log(self, script: str):
        """Carga el contenido del log del script."""
        log_file = f"logs/{script.replace('.py', '')}.log"
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                self.logs = f.read()[-2000:]
        else:
            self.logs = "No hay logs aún."

    def refresh_log(self):
        """Actualiza periódicamente el log del script actual."""
        if self.auto_update and self.current_script:
            self._load_log(self.current_script)
        return self

    def schedule_task(self, script: str, minutes: int):
        """Programa la ejecución periódica de un script."""
        job_id = f"{script}_job"
        scheduler.add_job(
            lambda: self.run_task(script),
            "interval",
            minutes=minutes,
            id=job_id,
            replace_existing=True,
        )
        self.message = f"Tarea '{script}' programada cada {minutes} minutos."
        return self

    def stop_task(self, script: str):
        """Detiene una tarea programada."""
        job_id = f"{script}_job"
        try:
            scheduler.remove_job(job_id)
            self.message = f"Tarea '{script}' detenida."
        except:
            self.message = "No hay tarea activa con ese nombre."
        return self
