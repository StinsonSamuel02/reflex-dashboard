#!/bin/bash
# ==========================================
# Script de actualización para Reflex Dashboard
# ==========================================

# Ruta del proyecto
PROJECT_DIR="/home/reflex-dashboard"
LOG_FILE="/var/log/supervisor/reflex_dashboard.log"
SUPERVISOR_PROGRAM="reflex-dashboard"

echo "🚀 Iniciando actualización de Reflex Dashboard..."
echo "=========================================="

# Cambiar al directorio del proyecto
cd "$PROJECT_DIR" || { echo "❌ Error: no se pudo acceder al directorio $PROJECT_DIR"; exit 1; }

# Hacer pull de la última versión
echo "📦 Ejecutando git pull..."
git pull || { echo "❌ Error en git pull"; exit 1; }

# Reiniciar el servicio de Supervisor
echo "🔁 Reiniciando servicio Supervisor ($SUPERVISOR_PROGRAM)..."
sudo supervisorctl restart "$SUPERVISOR_PROGRAM" || { echo "❌ Error al reiniciar Supervisor"; exit 1; }

# Esperar unos segundos para que arranque
sleep 2
echo "✅ Servicio reiniciado correctamente."
echo "=========================================="
echo "📜 Mostrando logs en tiempo real..."
echo "(Presiona Ctrl+C para salir)"
echo "=========================================="

# Mostrar logs
sudo tail -f "$LOG_FILE"
