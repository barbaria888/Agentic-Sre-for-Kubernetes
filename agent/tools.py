import subprocess

def run_cmd(cmd):
    return subprocess.getoutput(cmd)

def get_logs(pod_name):
    return run_cmd(f"kubectl logs {pod_name} --tail=50")

def restart_deploy(deploy_name):
    return run_cmd(f"kubectl rollout restart deployment {deploy_name}")
