def evaluate_result(result):
    result = result.lower()

    if any(x in result for x in ["error", "failed", "not found"]):
        return -1  # failure

    if any(x in result for x in ["restarted", "rollout restarted", "success"]):
        return 1  # success

    return 0  # unknown
