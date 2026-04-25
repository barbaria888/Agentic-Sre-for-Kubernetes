---
#  Agentic SRE for Kubernetes

![Kubernetes](https://img.shields.io/badge/Kubernetes-Automation-blue?logo=kubernetes)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)
![Ollama](https://img.shields.io/badge/LLM-Ollama%20\(Gemma\)-orange)
![ChromaDB](https://img.shields.io/badge/Memory-ChromaDB-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A Kubernetes-native **AI SRE automation agent** that detects pod failures, analyzes root cause using an LLM (Gemma via Ollama), and applies basic remediation using Kubernetes actions — with a memory layer for continuous learning.

---

## 🧠 What this project does

This system runs inside a Kubernetes cluster and continuously:

* Watches pod health
* Detects failures (CrashLoopBackOff, Pending, Error)
* Uses past incidents for context (ChromaDB)
* Sends structured context to an LLM (Gemma)
* Decides:

  * `restart`
  * `ignore`
* Executes remediation automatically
* Stores outcome for future decisions

---

## 🏗️ Architecture

```text
                          ┌──────────────────────┐
                          │   Kubernetes Cluster │
                          │  (Pods + Services)   │
                          └─────────┬────────────┘
                                    │
                                    ▼
                          ┌──────────────────────┐
                          │   Watcher (Python)   │
                          │  Kubernetes API Poll │
                          └─────────┬────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │   Issue Detection Layer     │
                     │ CrashLoopBackOff / Pending  │
                     └─────────┬───────────────────┘
                               │
                               ▼
             ┌────────────────────────────────────┐
             │        Memory Layer (ChromaDB)     │
             │   Past incidents + outcomes        │
             └─────────┬──────────────────────────┘
                       │
                       ▼
         ┌────────────────────────────────────────┐
         │     LLM Decision Engine (Gemma)        │
         │     via Ollama (http://ollama:11434)   │
         └─────────┬──────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────┐
        │   Decision: restart / ignore │
        └─────────┬────────────────────┘
                  │
                  ▼
        ┌──────────────────────────────┐
        │   Fixer (kubectl actions)    │
        │   restart deployment         │
        └─────────┬────────────────────┘
                  │
                  ▼
        ┌──────────────────────────────┐
        │  Evaluation + Feedback Loop  │
        │  Store in ChromaDB memory    │
        └──────────────────────────────┘
```

---

## ⚙️ Tech Stack

* Kubernetes (K3s / local cluster)
* Python 3.10
* FastAPI
* Ollama (Gemma 2B LLM)
* ChromaDB (vector memory store)
* SentenceTransformers
* kubectl CLI automation

---

## 📦 Project Structure

```bash
Agentic-SRE/
│
├── server.py        # FastAPI + background agent thread
├── main.py          # AI decision loop
├── watcher.py       # Kubernetes pod watcher
├── fixer.py         # remediation logic
├── memory.py        # ChromaDB memory layer
├── tools.py         # kubectl helpers
├── evaluator.py     # scoring system
├── requirements.txt
└── k8s/
```

---

## 🔄 Execution Flow

```text
Pod Failure
   ↓
Watcher detects issue
   ↓
Memory lookup (ChromaDB)
   ↓
Gemma LLM analysis (Ollama)
   ↓
Decision: restart / ignore
   ↓
kubectl action executed
   ↓
Result evaluated
   ↓
Stored back into memory
```

---

## 🌐 API Endpoints

### Health Check

```http
GET /
```

### Debug Pods

```http
GET /pods
```

---

## 🚀 Deployment

### Apply Kubernetes manifests

```bash
kubectl apply -f k8s/
```

### Check pods

```bash
kubectl get pods
```

### View logs

```bash
kubectl logs -f deploy/ai-agent
```

---

## 🧪 Testing

### Test Ollama + Gemma

```bash
kubectl exec -it deploy/ai-agent -- curl http://ollama:11434/api/generate \
-d '{
  "model": "gemma:2b",
  "prompt": "Say hello",
  "stream": false
}'
```

---

## 💾 Memory System

Each incident is stored as:

```text
Pod: nginx-xyz
Namespace: default
Issue: CrashLoopBackOff
Action: restart
Result: success/failure
Score: +1 / -1
```

---

## ⚠️ Known Issues

### 1. Chroma connection errors

* Ensure service is reachable:

```text
http://chroma:8000
```

### 2. LangChain deprecation warning

Replace:

```python
from langchain_community.llms import Ollama
```

with:

```python
from langchain_ollama import OllamaLLM
```

### 3. Startup race condition

Chroma may not be ready when agent starts → retry logic required

---

## 🔮 Future Improvements

* Event-driven Kubernetes watcher (no polling)
* Prometheus + alert integration
* UI dashboard for incidents
* Stronger scoring / RL-based feedback loop
* Replace kubectl with Kubernetes Python client

---
👨‍💻 Purpose of this project

This is a cloud-native learning system, built to explore:

AI in DevOps workflows
Kubernetes automation patterns
LLM-driven decision systems (Gemma via Ollama)
Self-healing infrastructure concepts
Vector database–powered incident memory (ChromaDB)
AI inference pipelines inside Kubernetes environments
---
