from watcher import watch_pods
from fixer import detect_issue, fix_issue
from memory import search_similar
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    base_url="http://ollama:11434",
    model="gemma:2b"
)


def format_memory(memories):
    memories = sorted(memories, key=lambda x: x["score"], reverse=True)
    return "\n".join([f"{m['score']}: {m['text']}" for m in memories])


def clean_decision(text):
    text = text.lower()

    if "restart" in text:
        return "restart"
    return "ignore"


def analyze(pod):
    memories = search_similar(pod["status"])
    context = format_memory(memories)

    prompt = f"""
You are a Kubernetes SRE agent.

Pod: {pod['name']}
Namespace: {pod['namespace']}
Status: {pod['status']}

Past incidents:
{context}

Return ONLY: restart or ignore
"""

    try:
        response = llm.invoke(prompt)
        return clean_decision(response)
    except Exception as e:
        print("LLM error:", e)
        return "ignore"


def run_loop():
    print("🚀 AI SRE Agent started")

    seen = set()

    for pod in watch_pods():
        key = f"{pod['namespace']}/{pod['name']}"

        if key in seen:
            continue

        seen.add(key)

        print(f"\n⚠️ Event: {pod}")

        if detect_issue(pod):
            print("🔍 analyzing...")
            decision = analyze(pod)
            print("🧠 decision:", decision)

            print("🛠 executing...")
            result = fix_issue(pod, decision)
            print("✅ result:", result)
