"""
Pipeline de indexação RAG:
1. Lê todos os PDFs do diretório pdfs/
2. Divide o texto em chunks com overlap
3. Gera embeddings usando text-embedding-004 (Google)
4. Armazena no ChromaDB (vector store persistido em disco)

Uso: python agents/rag_agent/build_index.py
"""

import os
import sys
import time

from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()

PDFS_DIR = os.path.join(os.path.dirname(__file__), "pdfs")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "investments"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
EMBEDDING_MODEL = "gemini-embedding-001"
BATCH_SIZE = 50


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def chunk_text(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 1 <= chunk_size:
            current_chunk += (" " if current_chunk else "") + paragraph
        else:
            if current_chunk:
                chunks.append(current_chunk)
            if len(paragraph) > chunk_size:
                words = paragraph.split()
                current_chunk = ""
                for word in words:
                    if len(current_chunk) + len(word) + 1 <= chunk_size:
                        current_chunk += (" " if current_chunk else "") + word
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = word
            else:
                overlap_text = current_chunk[-overlap:] if current_chunk else ""
                current_chunk = (
                    overlap_text + " " + paragraph if overlap_text else paragraph
                )

    if current_chunk:
        chunks.append(current_chunk)

    return [c.strip() for c in chunks if c.strip()]


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    from google import genai

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERRO: GOOGLE_API_KEY nao encontrada no .env")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    all_embeddings = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch,  # type: ignore
        )
        batch_embeddings = [e.values for e in result.embeddings]  # type: ignore
        all_embeddings.extend(batch_embeddings)

        if i + BATCH_SIZE < len(texts):
            time.sleep(0.5)

    return all_embeddings


def build_index():
    import chromadb

    print("=" * 60)
    print("  RAG Index Builder - Pipeline de Indexacao")
    print("=" * 60)

    # Step 1: Ler PDFs
    print("\n[1/4] Lendo PDFs...")
    pdf_files = sorted([f for f in os.listdir(PDFS_DIR) if f.endswith(".pdf")])

    if not pdf_files:
        print(f"ERRO: Nenhum PDF encontrado em {PDFS_DIR}")
        sys.exit(1)

    documents = {}
    for pdf_file in pdf_files:
        path = os.path.join(PDFS_DIR, pdf_file)
        text = extract_text_from_pdf(path)
        documents[pdf_file] = text
        print(f"  {pdf_file}: {len(text)} caracteres")

    # Step 2: Chunking
    print(
        f"\n[2/4] Dividindo em chunks (tamanho={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})..."
    )
    all_chunks = []
    all_metadatas = []
    all_ids = []

    for pdf_file, text in documents.items():
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append(
                {
                    "source": pdf_file,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                }
            )
            all_ids.append(f"{pdf_file}__chunk_{i:04d}")

    print(f"  Total de chunks: {len(all_chunks)}")
    print(f"  Media de chunks por documento: {len(all_chunks) / len(documents):.0f}")

    # Step 3: Embeddings
    print(f"\n[3/4] Gerando embeddings com {EMBEDDING_MODEL}...")
    print(f"  Processando {len(all_chunks)} chunks em batches de {BATCH_SIZE}...")
    embeddings = generate_embeddings(all_chunks)
    print(f"  Dimensao do embedding: {len(embeddings[0])}")

    # Step 4: ChromaDB
    print(f"\n[4/4] Salvando no ChromaDB ({CHROMA_DIR})...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    existing = client.list_collections()
    if any(c.name == COLLECTION_NAME for c in existing):
        client.delete_collection(COLLECTION_NAME)
        print(f"  Colecao '{COLLECTION_NAME}' anterior removida.")

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    for i in range(0, len(all_chunks), BATCH_SIZE):
        end = min(i + BATCH_SIZE, len(all_chunks))
        collection.add(
            ids=all_ids[i:end],
            embeddings=embeddings[i:end],  # type: ignore
            documents=all_chunks[i:end],
            metadatas=all_metadatas[i:end],
        )

    print(f"  Colecao '{COLLECTION_NAME}' criada com {collection.count()} documentos.")

    print("\n" + "=" * 60)
    print("  Indexacao concluida com sucesso!")
    print("  Agora rode: adk web agents/")
    print("=" * 60)


if __name__ == "__main__":
    build_index()
