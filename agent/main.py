from watcher import watch_pods
from fixer import detect_issue, fix_issue
from memory import search_similar
from langchain.llms import Ollama
import time

llm = Ollama(base_url="http://ollama:11434", model="gemma:2b")

def format_memory(memories):
    # 🔥 prioritize good outcomes
    sorted_mem = sorted(memories, key=lambda x: x["score"], reverse=True)

    text = ""
    for m in sorted_mem:
        text += f"\nScore: {m['score']}\n{m['text']}\n"

    return text

def analyze_with_llm(pod):
    memories = search_similar(pod["status"])

    context = format_memory(memories)

    prompt = f"""
    You are an SRE agent.

    Current issue:
    Pod {pod['name']} in {pod['namespace']} is {pod['status']}

    Past incidents (higher score = better outcome):
    {context}

    Prefer actions with HIGH score.
    Avoid actions with NEGATIVE score.

    Respond with ONE word:
    restart | ignore
    """

    return llm(prompt)

def run_loop():
    print("🚀 Auto-remediation agent started...")

    for pod in watch_pods():
        print(f"\n⚠️ Detected: {pod}")

        if detect_issue(pod):
            print("🔍 Analyzing...")
            suggestion = analyze_with_llm(pod)
            print("🧠 Suggestion:", suggestion)

            print("🛠 Fixing...")
            result = fix_issue(pod)
            print("✅ Result:", result)

        time.sleep(2)

if __name__ == "__main__":
    run_loop()
