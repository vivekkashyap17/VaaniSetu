# BhashaBridge backend — CPU-only inference image.
FROM python:3.11-slim

# Keep Python output unbuffered and skip .pyc files.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first for better layer caching.
# torch is pinned to the +cpu build, which lives on the PyTorch CPU index.
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Application code (config comes from the environment at runtime, not baked in).
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
