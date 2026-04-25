import chromadb
from chromadb.utils import embedding_functions

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.HttpClient(host="chroma", port=8000)

collection = client.get_or_create_collection(
    name="sre-memory",
    embedding_function=embedding_func
)

def store_incident(pod, issue, action, result, score):
    doc = f"""
    Pod: {pod['name']}
    Namespace: {pod['namespace']}
    Issue: {issue}
    Action: {action}
    Result: {result}
    Score: {score}
    """

    collection.add(
        documents=[doc],
        metadatas=[{"score": score}],
        ids=[f"{pod['name']}-{len(doc)}"]
    )

def search_similar(issue, k=5):
    res = collection.query(
        query_texts=[issue],
        n_results=k
    )

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]

    #  attach score to each result
    enriched = []
    for d, m in zip(docs, metas):
        enriched.append({
            "text": d,
            "score": m.get("score", 0)
        })

    return enriched
