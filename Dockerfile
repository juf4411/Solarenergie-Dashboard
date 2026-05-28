FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY solar_config ./solar_config
COPY solar_fetcher ./solar_fetcher
COPY solar_processing ./solar_processing
COPY solar_server ./solar_server
COPY solar_storage ./solar_storage
RUN pip install --no-cache-dir ".[test]"

COPY . .

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "solar_server.server:app", "--host", "0.0.0.0", "--port", "8000"]
