from watcher import watch_pods
from fixer import detect_issue, fix_issue
from langchain.llms import Ollama
import time

llm = Ollama(base_url="http://ollama:11434", model="gemma:2b")

def analyze_with_llm(pod):
    prompt = f"""
    You are an SRE agent.
    Pod {pod['name']} in namespace {pod['namespace']} is in state {pod['status']}.
    Suggest a simple safe fix in one short line.
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
