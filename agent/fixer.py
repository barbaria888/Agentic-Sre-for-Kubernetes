from tools import get_logs, restart_deploy
from memory import store_incident

restart_count = {}

def detect_issue(pod):
    bad_states = ["CrashLoopBackOff", "Error", "Failed", "Pending"]
    return pod["status"] in bad_states

def fix_issue(pod):
    name = pod["name"]
    issue = pod["status"]

    if restart_count.get(name, 0) > 3:
        return "⛔ Skipped (too many restarts)"

    logs = get_logs(name)

    if "CrashLoopBackOff" in logs or "Error" in logs:
        deploy = name.split("-")[0]
        restart_count[name] = restart_count.get(name, 0) + 1

        result = restart_deploy(deploy)

        # ✅ store in vector DB
        store_incident(pod, issue, "restart", result)

        return result

    store_incident(pod, issue, "none", "no_action")
    return "ℹ️ No action taken"
