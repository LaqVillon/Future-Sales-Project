FROM python:3.12

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /etl/requirements.txt

RUN pip install --no-cache-dir -r /etl/requirements.txt

# Copy the rest of your application's code
COPY . /etl

WORKDIR /etl

# Set the default command to run the ETL simulator script
ENTRYPOINT ["python", "etl_simulator.py"]
