FROM python:3.12

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of your application's code
COPY . /app

WORKDIR /app

EXPOSE 5000

CMD ["python", "api.py", "--host=0.0.0.0", "--port=5000"]
