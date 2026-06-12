FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip wheel && pip install --no-cache-dir -r requirements.txt
COPY service/ ./service/

RUN useradd --uid 1000 -m theia && chown -R theia:theia /app
USER theia

EXPOSE 8000
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]