# ------------ Build image ------------
FROM python:3.12-slim

# -- Runtime hygiene
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# OS packages needed by psycopg2, Pillow, etc.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc pkg-config \
        default-libmysqlclient-dev \   # <-- new
        netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*



# Install Python deps first (keeps layers small on code changes)
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy project code
COPY . .

# Copy entrypoint script into the image
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Entrypoint takes care of migrations, static files, worker, etc.
ENTRYPOINT ["/entrypoint.sh"]
