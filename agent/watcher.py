def watch_pods():
    w = watch.Watch()

    for event in w.stream(v1.list_pod_for_all_namespaces):
        pod = event["object"]

        try:
            yield {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase
            }
        except Exception:
            continue
