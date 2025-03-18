# Configuración de Gunicorn optimizada para Raspberry Pi 4

# Servidor
bind = "0.0.0.0:5000"
backlog = 256  # Reducido para Raspberry Pi

# Procesos de trabajo e hilos
workers = 1
worker_class = "gthread"
threads = 4
worker_connections = 250  # Reducido para Raspberry Pi
timeout = 180
keepalive = 2

# Reinicio periódico para evitar fugas de memoria
max_requests = 1000
max_requests_jitter = 50

# Opciones de seguridad
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = "-"  # Envía logs de acceso a stdout
errorlog = "-"   # Envía logs de error a stderr
loglevel = "info"

# Modo de precarga (desactivado para reducir uso de memoria)
preload_app = False

# Configuración específica para hardware limitado
graceful_timeout = 30