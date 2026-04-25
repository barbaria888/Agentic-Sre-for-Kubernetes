FROM python:3.10-slim

WORKDIR /app
COPY . .

# install kubectl
RUN apt-get update && apt-get install -y curl \
 && curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl" \
 && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
 && rm kubectl \
 && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python main.py & uvicorn server:app --host 0.0.0.0 --port 8000"]
