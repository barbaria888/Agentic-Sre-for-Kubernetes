from watcher import watch_pods
from fixer import detect_issue, fix_issue
from memory import search_similar
from langchain.llms import Ollama
import time

llm = Ollama(base_url="http://ollama:11434", model="gemma:2b")

def analyze_with_llm(pod):
    similar = search_similar(pod["status"])

    prompt = f"""
    You are an SRE agent.

    Current issue:
    Pod {pod['name']} in {pod['namespace']} is {pod['status']}

    Similar past incidents:
    {similar}

    Respond with ONE word:
    restart | ignore
    """

    return llm(prompt)

def run_loop():
    print(" Auto-remediation agent started...")

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
