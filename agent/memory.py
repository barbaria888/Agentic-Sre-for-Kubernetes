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

def store_incident(pod, issue, action, result):
    doc = f"""
    Pod: {pod['name']}
    Namespace: {pod['namespace']}
    Issue: {issue}
    Action: {action}
    Result: {result}
    """

    collection.add(
        documents=[doc],
        ids=[f"{pod['name']}-{len(doc)}"]
    )

def search_similar(issue, k=3):
    res = collection.query(
        query_texts=[issue],
        n_results=k
    )

    return res.get("documents", [[]])[0]
