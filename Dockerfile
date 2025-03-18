# Imagen base de Python
FROM python:3.9-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Crear usuario no privilegiado para seguridad
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Crear y establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Corrección de permisos
RUN chown -R appuser:appgroup /app

# Cambiar al usuario no privilegiado
USER appuser

# Exponer puerto
EXPOSE 5000

# Comando para iniciar Gunicorn con archivo de configuración
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]