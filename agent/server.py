from fastapi import FastAPI
from watcher import watch_pods

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/pods")
def list_pods():
    pods = []
    for i, pod in enumerate(watch_pods()):
        pods.append(pod)
        if i > 5:
            break
    return pods
