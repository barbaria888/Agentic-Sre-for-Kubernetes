from tools import get_logs, restart_deploy

restart_count = {}

def detect_issue(pod):
    bad_states = ["CrashLoopBackOff", "Error", "Failed", "Pending"]
    return pod["status"] in bad_states

def fix_issue(pod):
    name = pod["name"]

    if restart_count.get(name, 0) > 3:
        return "⛔ Skipped (too many restarts)"

    logs = get_logs(name)

    if "CrashLoopBackOff" in logs or "Error" in logs:
        deploy = name.split("-")[0]
        restart_count[name] = restart_count.get(name, 0) + 1
        return restart_deploy(deploy)

    return "ℹ️ No action taken"
