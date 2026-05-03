# Bloco 2 — Agente RAG com Busca Semântica Vetorial

Neste bloco vamos construir um agente de **RAG real** — com PDFs, embeddings, vector store e busca por similaridade semântica. Nada de mock ou keyword search: vamos usar exatamente o que se usa em produção.

## 2.1 O que é RAG?

**RAG (Retrieval-Augmented Generation)** é um padrão arquitetural que combina:

1. **Retrieval**: buscar informações relevantes em uma base vetorial
2. **Augmented**: injetar o contexto encontrado no prompt do modelo
3. **Generation**: gerar resposta fundamentada nos dados reais

### Por que RAG?

LLMs têm duas limitações fundamentais:
- **Conhecimento congelado** — só sabem o que viram no treino
- **Alucinação** — inventam informações quando não sabem

RAG resolve ambas: o modelo responde **apenas** com base em dados que você controla.

### Arquitetura do nosso RAG

```
                  ┌─────────────────────────────────────────────┐
                  │          PIPELINE DE INDEXAÇÃO (offline)      │
                  │                                              │
                  │  PDFs ──▶ Chunking ──▶ Embeddings ──▶ ChromaDB │
                  └─────────────────────────────────────────────┘

                  ┌─────────────────────────────────────────────┐
                  │           PIPELINE DE BUSCA (runtime)         │
                  │                                              │
  Pergunta ──▶ Embedding ──▶ Similaridade ──▶ Top-K chunks       │
     │          da query      de cosseno      relevantes         │
     │                                            │              │
     ▼                                            ▼              │
  ┌──────────────────────────────────────────────────────────────┐
  │  Gemini recebe: pergunta + chunks como contexto              │
  │  Gera resposta fundamentada nos dados                        │
  └──────────────────────────────────────────────────────────────┘
```

## 2.2 Conceitos fundamentais

### Embeddings

Um **embedding** é uma representação numérica (vetor) do significado de um texto. Textos com significado similar têm vetores próximos no espaço vetorial.

```
"Tesouro Direto é um título público"  →  [0.12, -0.45, 0.78, ..., 0.33]  (3072 dimensões)
"Títulos do governo federal"          →  [0.11, -0.44, 0.79, ..., 0.31]  (vetor similar!)
"Receita de bolo de chocolate"        →  [0.89, 0.23, -0.56, ..., -0.71] (vetor distante)
```

Usamos o modelo `gemini-embedding-001` do Google, que gera vetores de **3072 dimensões**.

### Similaridade de cosseno

Para comparar dois vetores, usamos a **similaridade de cosseno** — mede o ângulo entre eles:
- **1.0** = idênticos (mesmo significado)
- **0.0** = sem relação
- **-1.0** = opostos

### Chunking

Documentos longos precisam ser divididos em **chunks** (pedaços) menores porque:
1. Embeddings perdem precisão em textos muito longos
2. Retornar um documento inteiro desperdiça contexto do modelo
3. Chunks menores = resultados mais precisos

Estratégia: chunks de ~500 caracteres com **overlap de 100** (sobreposição para não perder contexto nas bordas).

### Vector Store (ChromaDB)

O **ChromaDB** é um banco de dados vetorial que:
- Armazena embeddings + texto original + metadados
- Faz busca por similaridade de cosseno de forma eficiente (HNSW index)
- Persiste em disco (sobrevive restarts)

## 2.3 Estrutura do projeto

```
agents/rag_agent/
├── __init__.py
├── agent.py                    ← agente ADK
├── data/
│   ├── __init__.py
│   ├── pdfs/                   ← 10 PDFs sobre investimentos
│   │   ├── guia_renda_fixa.pdf
│   │   ├── guia_renda_variavel.pdf
│   │   ├── guia_fiis.pdf
│   │   ├── guia_etfs.pdf
│   │   ├── guia_fundos_investimento.pdf
│   │   ├── guia_gestao_carteira.pdf
│   │   ├── guia_analise_fundamentalista.pdf
│   │   ├── guia_planejamento_financeiro.pdf
│   │   ├── guia_tributacao_investimentos.pdf
│   │   └── guia_criptoativos.pdf
│   ├── build_index.py          ← script de indexação
│   ├── create_sample_pdfs.py   ← gera os PDFs (já rodado)
│   └── chroma_db/              ← vector store (gerado pelo build_index)
└── tools/
    ├── __init__.py
    └── rag_tools.py            ← tool de busca semântica
```

## 2.4 Criando a base de conhecimento (PDFs)


- Crie a base de PDFs:
```
python agents/rag_agent/create_sample_pdfs.py
```

- Crie os Índices:
```
python agents/rag_agent/build_index.py
```

Os PDFs já vêm no repositório com conteúdo denso sobre investimentos brasileiros. Cada guia cobre um tema em profundidade:

| PDF | Conteúdo |
|-----|----------|
| `guia_renda_fixa.pdf` | Tesouro Direto, CDB, LCI/LCA, Debêntures, CRI/CRA |
| `guia_renda_variavel.pdf` | Ações (ON/PN), B3, Dividendos, BDRs, IPO |
| `guia_fiis.pdf` | Tipos de FIIs, indicadores, riscos, montagem de carteira |
| `guia_etfs.pdf` | ETFs Brasil e internacionais, estratégias |
| `guia_fundos_investimento.pdf` | Classificação ANBIMA, avaliação, tributação |
| `guia_gestao_carteira.pdf` | Markowitz, alocação por perfil, rebalanceamento, comportamental |
| `guia_analise_fundamentalista.pdf` | Valuation, rentabilidade, endividamento, moats |
| `guia_planejamento_financeiro.pdf` | Reserva, orçamento, objetivos, erros comuns |
| `guia_tributacao_investimentos.pdf` | IR por classe, come-cotas, declaração IRPF |
| `guia_criptoativos.pdf` | Bitcoin, DeFi, como investir no Brasil |

> **Dica**: em produção, esses PDFs seriam documentos internos, papers, manuais, regulamentos — qualquer conhecimento proprietário do seu domínio.

## 2.5 Pipeline de indexação (build_index.py)

Este script roda **uma única vez** para processar os PDFs e criar o índice vetorial.

```bash
mkdir -p agents/rag_agent/data
```

```python
# agents/rag_agent/data/build_index.py

"""
Pipeline de indexação RAG:
1. Lê todos os PDFs do diretório data/pdfs/
2. Divide o texto em chunks com overlap
3. Gera embeddings usando gemini-embedding-001
4. Armazena no ChromaDB (vector store persistido em disco)
"""

import os
import sys
import time

import chromadb
from dotenv import load_dotenv
from google import genai
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
    """Extrai texto de todas as páginas de um PDF."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Divide texto em chunks com overlap para preservar contexto nas bordas."""
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
                # Parágrafo maior que chunk_size: dividir por palavras
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
                # Overlap: pegar os últimos N caracteres do chunk anterior
                overlap_text = current_chunk[-overlap:] if current_chunk else ""
                current_chunk = overlap_text + " " + paragraph if overlap_text else paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return [c.strip() for c in chunks if c.strip()]


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Gera embeddings em batch usando a API do Google."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERRO: GOOGLE_API_KEY não encontrada no .env")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    all_embeddings = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch,
        )
        batch_embeddings = [e.values for e in result.embeddings]
        all_embeddings.extend(batch_embeddings)

        if i + BATCH_SIZE < len(texts):
            time.sleep(0.5)  # Rate limiting

    return all_embeddings


def build_index():
    print("=" * 60)
    print("  RAG Index Builder - Pipeline de Indexação")
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
        print(f"  ✓ {pdf_file}: {len(text)} caracteres")

    # Step 2: Chunking
    print(f"\n[2/4] Dividindo em chunks (tamanho={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    all_chunks = []
    all_metadatas = []
    all_ids = []

    for pdf_file, text in documents.items():
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({
                "source": pdf_file,
                "chunk_index": i,
                "total_chunks": len(chunks),
            })
            all_ids.append(f"{pdf_file}__chunk_{i:04d}")

    print(f"  Total de chunks: {len(all_chunks)}")
    print(f"  Média por documento: {len(all_chunks) / len(documents):.0f}")

    # Step 3: Embeddings
    print(f"\n[3/4] Gerando embeddings com {EMBEDDING_MODEL}...")
    print(f"  Processando {len(all_chunks)} chunks em batches de {BATCH_SIZE}...")
    embeddings = generate_embeddings(all_chunks)
    print(f"  ✓ Dimensão do embedding: {len(embeddings[0])}")

    # Step 4: ChromaDB
    print(f"\n[4/4] Salvando no ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    existing = client.list_collections()
    if any(c.name == COLLECTION_NAME for c in existing):
        client.delete_collection(COLLECTION_NAME)
        print(f"  Coleção anterior removida.")

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    for i in range(0, len(all_chunks), BATCH_SIZE):
        end = min(i + BATCH_SIZE, len(all_chunks))
        collection.add(
            ids=all_ids[i:end],
            embeddings=embeddings[i:end],
            documents=all_chunks[i:end],
            metadatas=all_metadatas[i:end],
        )

    print(f"  ✓ Coleção '{COLLECTION_NAME}' criada com {collection.count()} documentos.")

    print("\n" + "=" * 60)
    print("  ✅ Indexação concluída! Rode: adk web agents/")
    print("=" * 60)


if __name__ == "__main__":
    build_index()
```

### O que cada etapa faz:

| Etapa | Descrição | Tecnologia |
|-------|-----------|------------|
| Leitura | Extrai texto de cada página do PDF | `pypdf` |
| Chunking | Divide em pedaços de ~500 chars com overlap de 100 | Python puro |
| Embeddings | Converte cada chunk em vetor de 3072 dimensões | `gemini-embedding-001` |
| Armazenamento | Salva vetores + texto + metadados em disco | ChromaDB |

### Rodando a indexação

```bash
python agents/rag_agent/data/build_index.py
```

Saída esperada:
```
============================================================
  RAG Index Builder - Pipeline de Indexação
============================================================

[1/4] Lendo PDFs...
  ✓ guia_analise_fundamentalista.pdf: 5747 caracteres
  ✓ guia_criptoativos.pdf: 4681 caracteres
  ...

[2/4] Dividindo em chunks (tamanho=500, overlap=100)...
  Total de chunks: 102
  Média por documento: 10

[3/4] Gerando embeddings com gemini-embedding-001...
  ✓ Dimensão do embedding: 3072

[4/4] Salvando no ChromaDB...
  ✓ Coleção 'investments' criada com 102 documentos.

============================================================
  ✅ Indexação concluída! Rode: adk web agents/
============================================================
```

## 2.6 Tool de busca semântica (rag_tools.py)

A tool que o agente usa em runtime para buscar informações:

```bash
mkdir -p agents/rag_agent/tools
touch agents/rag_agent/tools/__init__.py
```

```python
# agents/rag_agent/tools/rag_tools.py

import os

import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
COLLECTION_NAME = "investments"
EMBEDDING_MODEL = "gemini-embedding-001"
TOP_K = 5


def _get_collection():
    """Conecta ao ChromaDB e retorna a coleção de investimentos."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(name=COLLECTION_NAME)


def _embed_query(query: str) -> list[float]:
    """Gera embedding da pergunta do usuário usando o mesmo modelo da indexação."""
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
    )
    return result.embeddings[0].values


def search_knowledge_base(query: str) -> dict:
    """Busca informações na base de conhecimento sobre investimentos usando busca semântica.

    Usa embeddings e similaridade de cosseno para encontrar os trechos mais relevantes
    na base vetorial de documentos sobre investimentos brasileiros.

    Args:
        query: Pergunta ou termo para buscar na base de conhecimento.

    Returns:
        dict com os resultados encontrados, incluindo fonte, conteúdo e score de relevância.
    """
    try:
        collection = _get_collection()
    except Exception:
        return {
            "status": "error",
            "message": "Índice não encontrado. Execute: python agents/rag_agent/data/build_index.py",
            "results": [],
        }

    # Gera embedding da query (mesmo modelo usado na indexação)
    query_embedding = _embed_query(query)

    # Busca os TOP_K chunks mais similares
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    # Formata resultados com score de similaridade
    formatted_results = []
    for i in range(len(results["documents"][0])):
        doc = results["documents"][0][i]
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        similarity = 1 - distance  # Converte distância em similaridade

        formatted_results.append({
            "content": doc,
            "source": metadata["source"].replace(".pdf", "").replace("_", " ").title(),
            "similarity_score": round(similarity, 3),
        })

    return {
        "status": "success",
        "message": f"{len(formatted_results)} trecho(s) relevante(s) encontrado(s).",
        "query": query,
        "results": formatted_results,
    }
```

### Como a busca funciona:

```
Pergunta: "Quais os riscos de investir em FIIs?"
                    │
                    ▼
        ┌───────────────────────┐
        │ Embedding da query    │ → [0.23, -0.67, 0.41, ..., 0.88]
        │ (gemini-embedding-001)│
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ ChromaDB: busca os 5  │ → Compara com 102 embeddings armazenados
        │ vetores mais próximos │   usando similaridade de cosseno
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ Retorna top-5 chunks  │ → score: 0.78, 0.72, 0.69, 0.65, 0.61
        │ com fonte e score     │
        └───────────────────────┘
```

## 2.7 Criando o agente RAG

```bash
mkdir -p agents/rag_agent
touch agents/rag_agent/__init__.py
```

```python
# agents/rag_agent/agent.py

from google.adk.agents import Agent
from .tools.rag_tools import search_knowledge_base

from dotenv import load_dotenv

load_dotenv()

rag_agent = Agent(
    name="rag_agent",
    model="gemini-2.5-flash",
    description="Agente especializado em buscar e explicar informações sobre investimentos usando RAG com busca semântica vetorial.",
    instruction="""
    Você é um agente de RAG (Retrieval-Augmented Generation) especializado em investimentos no mercado financeiro brasileiro.

    Você tem acesso a uma base de conhecimento vetorial com documentos sobre: renda fixa, renda variável, ações, FIIs,
    ETFs, fundos de investimento, gestão de carteira, análise fundamentalista, planejamento financeiro, tributação e criptoativos.

    REGRAS:
    1. SEMPRE use a ferramenta search_knowledge_base antes de responder qualquer pergunta sobre investimentos
    2. Baseie suas respostas EXCLUSIVAMENTE nos dados retornados pela busca semântica
    3. Cite a fonte do documento quando relevante (ex: "Segundo o Guia de Renda Fixa...")
    4. Se os resultados retornados não forem suficientes, faça uma segunda busca com termos diferentes
    5. Se não encontrar informações na base, diga claramente que não tem essa informação disponível
    6. Responda de forma educacional, clara e estruturada
    7. Use exemplos práticos quando possível para ilustrar conceitos
    8. Sempre mencione que suas respostas são educacionais e não constituem recomendação de investimento

    Você é o especialista em conhecimento teórico sobre investimentos do nosso sistema multi-agente.
    """,
    tools=[search_knowledge_base],
)
```

```python
# agents/rag_agent/__init__.py

from .agent import rag_agent

root_agent = rag_agent
```

## 2.8 Testando o agente

### Passo 1 — Indexar os documentos

```bash
python agents/rag_agent/data/build_index.py
```

### Passo 2 — Rodar a interface web

```bash
adk web agents/
```

Selecione **rag_agent** e teste:

| Pergunta | O que acontece |
|----------|----------------|
| "O que é Tesouro Direto?" | Busca semântica → chunks sobre Tesouro → resposta fundamentada |
| "Quais os riscos de FIIs?" | Encontra seção de riscos no guia de FIIs |
| "Como funciona a tributação de ações?" | Retorna chunks do guia de tributação |
| "Me explica o que são moats" | Busca no guia de análise fundamentalista |
| "Qual a melhor alocação para perfil moderado?" | Encontra alocação por perfil no guia de gestão |
| "O que é DeFi?" | Chunks do guia de criptoativos |
| "Como declarar Bitcoin no IR?" | Cruza info de cripto + tributação |

### Comparação: keyword search vs busca semântica

| Pergunta | Keyword (antigo) | Semântica (novo) |
|----------|-----------------|------------------|
| "Como proteger meu dinheiro da inflação?" | ❌ Não encontra (nenhuma keyword match) | ✅ Retorna Tesouro IPCA+, diversificação |
| "Quero renda passiva mensal" | ❌ Falha | ✅ Retorna FIIs, dividendos |
| "Investimento seguro para emergência" | ❌ Parcial | ✅ Tesouro Selic, reserva de emergência |
| "Vale a pena day trade?" | ❌ Não encontra | ✅ Tributação day trade, finanças comportamentais |

A busca semântica entende **intenção**, não apenas palavras.

## 2.9 Como o RAG funciona por baixo (passo a passo)

Quando você pergunta "Quais os riscos de investir em FIIs?":

```
1. Agente recebe a pergunta
2. Gemini decide chamar search_knowledge_base(query="riscos FIIs investimento")
3. A tool gera o embedding da query via gemini-embedding-001
4. ChromaDB calcula similaridade de cosseno com os 102 chunks indexados
5. Retorna os 5 chunks mais similares (com score > 0.65)
6. Agente recebe: chunks sobre vacância, inadimplência, mercado, crédito, concentração
7. Gemini usa esse contexto + pergunta original para gerar resposta estruturada
8. Usuário recebe resposta fundamentada com citação da fonte
```

O modelo **decide sozinho** quando chamar a tool — isso é **function calling** em ação.

## 2.10 Conceitos-chave aprendidos

| Conceito | Descrição |
|----------|-----------|
| RAG | Busca vetorial + contexto + geração — elimina alucinações |
| Embeddings | Representação numérica do significado de um texto |
| Similaridade de cosseno | Métrica que mede proximidade semântica entre vetores |
| Chunking com overlap | Divisão de documentos preservando contexto nas bordas |
| Vector Store (ChromaDB) | Banco de dados otimizado para busca por similaridade |
| Pipeline de indexação | Processo offline: PDF → chunks → embeddings → vector store |
| Busca semântica | Encontra resultados por significado, não por keywords exatas |
| Function Calling | O modelo decide quando e como chamar a tool de busca |

## 2.11 Indo além (para quem quiser explorar depois)

- **Adicionar seus próprios PDFs**: coloque qualquer PDF em `data/pdfs/` e rode `build_index.py` novamente
- **Ajustar chunk_size**: chunks menores = mais preciso; maiores = mais contexto
- **Aumentar TOP_K**: retornar mais resultados (trade-off: mais contexto vs. mais ruído)
- **Hybrid search**: combinar busca semântica com keyword para melhores resultados
- **Re-ranking**: usar um modelo de re-ranking após a busca inicial
- **Metadata filtering**: filtrar por fonte antes da busca (ex: só buscar no guia de RF)

No próximo bloco vamos construir os agentes de mercado e relatório. Vamos para o [Bloco 3](BLOCO-3.md).
