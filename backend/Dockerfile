# VaaniSetu backend — CPU-only inference image.
FROM python:3.11-slim

# Keep Python output unbuffered, skip .pyc files, and never cache pip downloads.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install dependencies first for better layer caching.
# torch is pinned to the +cpu build, which lives on the PyTorch CPU index.
# Everything below runs in ONE layer so the uninstall/cleanup actually shrinks
# the final image instead of just masking files in a later layer.
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt && \
    # Strip build-only and doc-only packages pulled in transitively (e.g. by
    # indic-nlp-library-itt). None of these are imported at runtime; removing
    # them here reclaims ~100 MB. `|| true` keeps the build green if a name is
    # absent on a given resolve.
    pip uninstall -y \
        Cython \
        Sphinx sphinx-rtd-theme sphinx-argparse \
        sphinxcontrib-applehelp sphinxcontrib-devhelp sphinxcontrib-htmlhelp \
        sphinxcontrib-jsmath sphinxcontrib-qthelp sphinxcontrib-serializinghtml \
        sphinxcontrib-jquery \
        alabaster babel imagesize snowballstemmer docutils \
        2>/dev/null || true && \
    # Drop bytecode caches left by the installs.
    find /usr/local/lib/python3.11/site-packages -type d -name "__pycache__" -prune -exec rm -rf {} + && \
    rm -rf /root/.cache

# Application code (config comes from the environment at runtime, not baked in).
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
