import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
COLLECTION_NAME = "investments"
EMBEDDING_MODEL = "gemini-embedding-001"
TOP_K = 5


def _get_collection():
    import chromadb

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(name=COLLECTION_NAME)


def _embed_query(query: str) -> list[float]:
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
    )
    return result.embeddings[0].values  # type: ignore


def search_knowledge_base(query: str) -> dict:
    """Busca informacoes na base de conhecimento sobre investimentos usando busca semantica.

    Usa embeddings e similaridade de cosseno para encontrar os trechos mais relevantes
    na base vetorial de documentos sobre investimentos brasileiros.

    Args:
        query: Pergunta ou termo para buscar na base de conhecimento.

    Returns:
        dict com os resultados encontrados, incluindo fonte, conteudo e score de relevancia.
    """
    try:
        collection = _get_collection()
    except Exception:
        return {
            "status": "error",
            "message": "Indice nao encontrado. Execute: python agents/rag_agent/build_index.py",
            "results": [],
        }

    query_embedding = _embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    formatted_results = []
    for i in range(len(results["documents"][0])):  # type: ignore
        doc = results["documents"][0][i]  # type: ignore
        metadata = results["metadatas"][0][i]  # type: ignore
        distance = results["distances"][0][i]  # type: ignore
        similarity = 1 - distance

        formatted_results.append(
            {
                "content": doc,
                "source": metadata["source"]
                .replace(".pdf", "")  # type: ignore
                .replace("_", " ")
                .title(),
                "similarity_score": round(similarity, 3),
            }
        )

    return {
        "status": "success",
        "message": f"{len(formatted_results)} trecho(s) relevante(s) encontrado(s).",
        "query": query,
        "results": formatted_results,
    }
