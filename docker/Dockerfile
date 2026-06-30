FROM python:3.12-slim

# ---------------------------------------
# Environment
# ---------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------------------------------------
# Install OS packages
# ---------------------------------------

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------
# Create non-root user
# ---------------------------------------

RUN useradd -m appuser

# ---------------------------------------
# Working directory
# ---------------------------------------

WORKDIR /app

# ---------------------------------------
# Copy requirements first
# ---------------------------------------

COPY stockanalyzer/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------------------
# Copy source
# ---------------------------------------

COPY stockanalyzer/ .

# ---------------------------------------
# Ownership
# ---------------------------------------

RUN chown -R appuser:appuser /app

USER appuser

# ---------------------------------------
# Expose
# ---------------------------------------

EXPOSE 8000

# ---------------------------------------
# Health Check
# ---------------------------------------

HEALTHCHECK \
--interval=30s \
--timeout=10s \
--start-period=20s \
--retries=3 \
CMD curl -f http://localhost:8000/health || exit 1

# ---------------------------------------
# Start FastAPI
# ---------------------------------------

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
