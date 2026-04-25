from tools import get_logs, restart_deploy
from memory import store_incident, search_similar
from evaluator import evaluate_result

restart_count = {}

def detect_issue(pod):
    bad_states = ["CrashLoopBackOff", "Error", "Failed", "Pending"]
    return pod["status"] in bad_states


def fix_issue(pod, suggestion="restart"):
    name = pod["name"]
    issue = pod["status"]

    if restart_count.get(name, 0) > 3:
        return "⛔ Skipped (too many restarts)"

    logs = get_logs(name).lower()

    # 🔥 use logs
    if "oomkilled" in logs:
        store_incident(pod, issue, "ignore", "oom_detected", -1)
        return "⚠️ OOM detected — restart skipped"

    # 🧠 memory guard
    memories = search_similar(issue)
    if memories:
        avg_score = sum(m["score"] for m in memories) / len(memories)
    else:
        avg_score = 0

    if avg_score < 0:
        store_incident(pod, issue, "blocked_restart", "memory_negative", -1)
        return "⛔ Blocked by memory (bad past outcomes)"

    # 🤖 LLM suggestion
    if suggestion.strip().lower().startswith("restart"):
        deploy = name.split("-")[0]
        restart_count[name] = restart_count.get(name, 0) + 1

        result = restart_deploy(deploy)

        score = evaluate_result(result)

        store_incident(pod, issue, "restart", result, score)

        return result

    store_incident(pod, issue, "none", "no_action", 0)
    return "ℹ️ No action taken"
