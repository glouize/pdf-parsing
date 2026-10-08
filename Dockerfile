# Stage 1: builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir build && python -m build --wheel

# Stage 2: runtime
FROM python:3.11-slim
WORKDIR /app
# Install system dependencies for Tesseract OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/dist/*.whl .
RUN pip install --no-cache-dir *.whl && rm *.whl
COPY alembic.ini .
COPY src/pdf_parsing/db/migrations src/pdf_parsing/db/migrations
EXPOSE 8050
CMD ["python", "-m", "pdf_parsing.dashboard.app"]
