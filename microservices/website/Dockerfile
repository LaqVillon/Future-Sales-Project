FROM python:3.12

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /website/requirements.txt

RUN pip install --no-cache-dir -r /website/requirements.txt

# Copy the rest of your application's code
COPY . /website

WORKDIR /website

EXPOSE 8080

CMD ["python", "website.py", "--host=0.0.0.0", "--port=8080"]