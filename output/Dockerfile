# Stage 1: Builder - Install dependencies and build application artifacts
FROM python:3.9-slim-buster AS builder

# Security Rationale: Prevent Python from writing .pyc files and ensure logs are unbuffered.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Security Rationale: Install build dependencies required for Python packages (e.g., psycopg2).
# Use --no-install-recommends to minimize installed packages.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Security Rationale: Set a working directory inside the container.
WORKDIR /app

# Security Rationale: Copy requirements first to leverage Docker layer caching.
COPY requirements.txt .

# Security Rationale: Install Python dependencies. Use --no-cache-dir to reduce image size.
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image - Create a minimal runtime image
FROM python:3.9-slim-buster

# Security Rationale: Prevent Python from writing .pyc files and ensure logs are unbuffered.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Security Rationale: Install runtime dependencies for the application (e.g., libpq for PostgreSQL client).
# Use --no-install-recommends to minimize installed packages.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Security Rationale: Create a dedicated non-root user and group for the application.
# This adheres to the principle of least privilege, reducing the impact of a container compromise.
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Security Rationale: Set the working directory for the application.
WORKDIR /app

# Security Rationale: Copy only the necessary application code from the builder stage.
# This ensures the final image does not contain build tools or unnecessary files.
COPY --from=builder /app /app

# Security Rationale: Expose the port the application listens on.
# This does not publish the port to the host unless explicitly mapped in docker-compose.yml.
EXPOSE 8000

# Security Rationale: Define the command to run the application.
# Using gunicorn for a production-ready WSGI server.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_app_name.wsgi:application"]