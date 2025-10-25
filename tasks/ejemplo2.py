from datetime import datetime
import random

with open("logs/ejemplo2.log", "a") as f:
    f.write(f"[{datetime.now()}] Ejemplo2: valor aleatorio = {random.randint(1, 100)}\n")
