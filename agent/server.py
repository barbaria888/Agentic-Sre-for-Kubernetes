from contextlib import asynccontextmanager
from fastapi import FastAPI
from watcher import watch_pods
import threading
import time
import os
import requests


def wait_for_chroma(
    host=None,
    port=None,
    retries=None,
    delay=None,
):
    host = host or os.environ.get("CHROMA_HOST", "chroma")
    port = int(port or os.environ.get("CHROMA_PORT", "8000"))
    retries = int(retries or os.environ.get("CHROMA_RETRIES", "30"))
    delay = float(delay or os.environ.get("CHROMA_RETRY_DELAY", "2"))

    url = f"http://{host}:{port}/api/v1/heartbeat"
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                print("✅ Chroma ready")
                return
        except Exception as e:
            print(f"⏳ Waiting for Chroma... attempt {attempt}/{retries} | {type(e).__name__}: {e}")
        time.sleep(delay)
    raise RuntimeError(
        f"Chroma not ready after {retries} retries "
        f"(host={host}, port={port}) — aborting startup"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    wait_for_chroma()

    # 🔥 lazy import avoids startup race conditions
    from main import run_loop

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
