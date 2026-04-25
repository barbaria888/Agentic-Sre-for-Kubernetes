FROM python:3.10-slim

WORKDIR /app
COPY . .

# system deps
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# install kubectl
RUN curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl" \
 && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
 && rm kubectl

# python deps
RUN pip install --no-cache-dir -r requirements.txt

# run API + agent loop
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
