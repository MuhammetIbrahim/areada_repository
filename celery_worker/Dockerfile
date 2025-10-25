FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy uv requirements and install dependencies
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

# Copy source code
COPY . .

# Set Python path to find shared modules
ENV PYTHONPATH=/app

CMD ["uv", "run", "celery", "-A", "tasks", "worker", "--loglevel=info"]