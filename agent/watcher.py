from kubernetes import client, config, watch

config.load_incluster_config()
v1 = client.CoreV1Api()

def get_reason(pod):
    try:
        return pod.status.container_statuses[0].state.waiting.reason
    except:
        return pod.status.phase

def watch_pods():
    w = watch.Watch()
    for event in w.stream(v1.list_pod_for_all_namespaces):
        pod = event['object']

        yield {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": get_reason(pod)
        }
