from contextlib import asynccontextmanager
from fastapi import FastAPI
from watcher import watch_pods
from main import run_loop
import threading

@asynccontextmanager
async def lifespan(app: FastAPI):
    t = threading.Thread(target=run_loop, daemon=True)
    t.start()
    yield

app = FastAPI(lifespan=lifespan)

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
