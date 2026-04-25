import chromadb
import time
from chromadb.utils import embedding_functions
from chromadb.config import Settings

client = None
collection = None


def get_collection():
    global client, collection

    if collection:
        return collection

    for i in range(30):
        try:
            print(f"⏳ Connecting to Chroma... attempt {i+1}")

            client = chromadb.HttpClient(
                host="chroma",
                port=8000,
                settings=Settings(
                    anonymized_telemetry=False
                )
            )

            # ✅ critical fix
            client.heartbeat()

            # load embedding ONLY after connection works
            embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )

            collection = client.get_or_create_collection(
                name="sre-memory",
                embedding_function=embedding_func
            )

            print("✅ Connected to Chroma")
            return collection

        except Exception as e:
            print(f"❌ Chroma error type: {type(e).__name__} | {str(e)}")
            time.sleep(3)

    raise Exception("Chroma connection failed after retries")


def store_incident(pod, issue, action, result, score):
    try:
        col = get_collection()

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
            ids=[f"{pod['name']}-{int(time.time())}"]
        )

    except Exception as e:
        print("⚠️ Memory store failed:", e)


def search_similar(issue, k=5):
    try:
        col = get_collection()

        res = col.query(
            query_texts=[issue],
            n_results=k
        )

        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]

        return [
            {"text": d, "score": m.get("score", 0)}
            for d, m in zip(docs, metas)
        ]

    except Exception as e:
        print("⚠️ Memory search failed:", e)
        return []
