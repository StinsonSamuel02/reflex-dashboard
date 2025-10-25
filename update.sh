#!/bin/bash
# ==========================================
# Script de actualización y gestión de Reflex Dashboard
# ==========================================

# Configuración por defecto
PROJECT_DIR="/home/reflex-dashboard"
LOG_FILE="/var/log/supervisor/reflex_dashboard.log"
SUPERVISOR_PROGRAM="reflex-dashboard"

# ============================
# Funciones
# ============================

update_dashboard() {
  echo "🚀 Iniciando actualización de Reflex Dashboard..."
  echo "=========================================="

  # Cambiar al directorio del proyecto
  cd "$PROJECT_DIR" || {
    echo "❌ Error: no se pudo acceder al directorio $PROJECT_DIR"
    exit 1
  }

  # Hacer pull de la última versión
  echo "📦 Ejecutando git pull..."
  git pull || {
    echo "❌ Error en git pull"
    exit 1
  }

  # Reiniciar el servicio de Supervisor
  echo "🔁 Reiniciando servicio Supervisor ($SUPERVISOR_PROGRAM)..."
  sudo supervisorctl restart "$SUPERVISOR_PROGRAM" || {
    echo "❌ Error al reiniciar Supervisor"
    exit 1
  }

  # Esperar unos segundos para que arranque
  sleep 2
  echo "✅ Servicio reiniciado correctamente."
}

show_logs() {
  echo "📜 Mostrando logs en tiempo real..."
  echo "(Presiona Ctrl+C para salir)"
  echo "=========================================="
  sudo tail -f "$LOG_FILE"
}

# ============================
# Argumentos
# ============================
case "$1" in
update)
  update_dashboard
  ;;
logs)
  show_logs
  ;;
*)
  echo "Uso: $0 {update|logs}"
  exit 1
  ;;
esac
