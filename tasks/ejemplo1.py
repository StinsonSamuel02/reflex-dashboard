from datetime import datetime
import time

with open("logs/ejemplo1.log", "a") as f:
    f.write(f"[{datetime.now()}] Iniciando tarea ejemplo1...\n")
    time.sleep(3)
    f.write(f"[{datetime.now()}] Tarea ejemplo1 finalizada.\n")
