INSTALACIÓN PANEL REFLEX
========================

1. Crear entorno:
   cd /home/reflex_dashboard
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Inicializar Reflex:
   reflex init
   reflex export

3. Registrar configuración de Supervisor:
   sudo cp supervisor.conf /etc/supervisor/conf.d/reflex_dashboard.conf
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start reflex_dashboard

4. (Opcional) Registrar configuración de Nginx:
   sudo cp nginx.conf /etc/nginx/sites-available/reflex_dashboard
   sudo ln -s /etc/nginx/sites-available/reflex_dashboard /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx

5. Acceder al panel:
   http://<tu-ip>:8050

   Usuario: admin
   Contraseña: admin123
