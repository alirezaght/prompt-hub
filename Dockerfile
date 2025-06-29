FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends gcc libffi-dev libssl-dev && rm -rf /var/lib/apt/lists/*
RUN useradd -m user
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER user
ENV PORT=8080
ENV PYTHONPATH=/app/src
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080"]