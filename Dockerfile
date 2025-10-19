FROM python:3.9-slim

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]
