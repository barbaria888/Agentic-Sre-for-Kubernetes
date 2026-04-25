import chromadb
import time
from chromadb.utils import embedding_functions

# lazy init (DO NOT connect at import time)
client = None
collection = None


def get_client():
    global client, collection

    if client:
        return collection

    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    for i in range(15):
        try:
            print(f"⏳ Connecting to Chroma... attempt {i+1}")
            client = chromadb.HttpClient(host="chroma", port=8000)

            collection = client.get_or_create_collection(
                name="sre-memory",
                embedding_function=embedding_func
            )

            print("✅ Connected to Chroma")
            return collection

        except Exception as e:
            print("❌ Chroma not ready, retrying...")
            time.sleep(3)

    raise Exception("Chroma connection failed after retries")


def store_incident(pod, issue, action, result, score):
    col = get_client()

    doc = f"""
    Pod: {pod['name']}
    Namespace: {pod['namespace']}
    Issue: {issue}
    Action: {action}
    Result: {result}
    Score: {score}
    """

    col.add(
        documents=[doc],
        metadatas=[{"score": score}],
        ids=[f"{pod['name']}-{time.time()}"]
    )


def search_similar(issue, k=5):
    col = get_client()

    res = col.query(
        query_texts=[issue],
        n_results=k
    )

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]

    enriched = []
    for d, m in zip(docs, metas):
        enriched.append({
            "text": d,
            "score": m.get("score", 0)
        })

    return enriched
