# Bloco 1 — Google AI Studio: Conceitos e Playground

Neste bloco vamos explorar o [Google AI Studio](https://aistudio.google.com/) e entender cada conceito disponível no playground antes de escrever código.

## 1.1 Acessando o Google AI Studio

1. Acesse [aistudio.google.com](https://aistudio.google.com/)
2. Faça login com sua conta Google
3. Clique em **"Create new prompt"** para abrir o playground

## 1.2 Conceitos do Playground

### Temperatura (`temperature`)

Controla a aleatoriedade das respostas do modelo.

- **0.0** — respostas determinísticas e focadas (ideal para tarefas objetivas)
- **1.0** — respostas mais criativas e variadas
- **2.0** — máxima aleatoriedade

> **Teste**: envie a mesma pergunta com temperatura 0 e depois com temperatura 1.5. Compare as respostas.

### Thinking Level

Controla o nível de "raciocínio" do modelo antes de responder.

- Modelos com thinking (como Gemini 2.5) podem "pensar" antes de responder
- Níveis mais altos = raciocínio mais profundo, mas mais lento e caro

> **Teste**: peça ao modelo para resolver um problema de lógica com e sem thinking ativado.

### Structured Outputs

Força o modelo a responder em um formato estruturado (JSON Schema).

- Útil para integrar a saída do modelo em sistemas programáticos
- Você define o schema e o modelo garante conformidade

> **Teste**: peça ao modelo para retornar informações de uma empresa no formato JSON com campos `nome`, `setor`, `ticker`.

### Code Execution

Permite ao modelo escrever e executar código Python em sandbox.

- O modelo pode fazer cálculos, gerar gráficos e processar dados
- A execução acontece em ambiente seguro do Google

> **Teste**: peça ao modelo para calcular o retorno composto de um investimento de R$10.000 a 12% a.a. por 5 anos.

### Function Calling

Permite ao modelo chamar funções que você define — é a base das **tools** no ADK.

- Você declara funções com nome, descrição e parâmetros
- O modelo decide quando chamar e com quais argumentos
- Você executa a função e retorna o resultado ao modelo

> **Teste**: declare uma função `get_stock_price(ticker: str)` e veja o modelo chamá-la.

### Grounding with Google Search

Permite ao modelo buscar informações atualizadas no Google Search.

- Reduz alucinações com dados em tempo real
- O modelo cita as fontes utilizadas

> **Teste**: pergunte "Qual a cotação atual do dólar?" com e sem grounding.

### Grounding with Google Maps

Permite ao modelo buscar informações geográficas e de localização.

- Dados de endereços, rotas, pontos de interesse
- Útil para agentes que lidam com localização

> **Teste**: pergunte "Onde fica a sede do Google no Brasil?" com grounding de Maps.

### URL Context

Permite ao modelo ler e analisar o conteúdo de URLs fornecidas.

- O modelo acessa a página e usa como contexto
- Útil para análise de artigos, documentações, relatórios

> **Teste**: passe a URL de uma notícia financeira e peça um resumo.

### Media Resolution

Controla a resolução de mídia (imagens, vídeos) processada pelo modelo.

- Resoluções mais altas = mais detalhes, mas mais tokens consumidos
- Escolha baseado na necessidade de detalhe vs. custo

### Safety Settings

Configura os filtros de segurança do modelo.

- Categorias: assédio, discurso de ódio, conteúdo sexual, conteúdo perigoso
- Níveis: bloquear nenhum, poucos, alguns, maioria

> **Atenção**: para workshop educacional, mantenha as configurações padrão.

### Add Stop Sequence

Define sequências de texto que fazem o modelo parar de gerar.

- Útil para controlar o formato de saída
- Exemplo: `\n\n` para parar após dois parágrafos

### Output Length (Max Tokens)

Limita o número máximo de tokens na resposta.

- Controla custo e tamanho da resposta
- Não significa que o modelo vai usar todos os tokens — é um limite

### Top-P (Nucleus Sampling)

Controla a diversidade da saída por amostragem de núcleo.

- **0.1** — considera apenas os tokens mais prováveis (mais focado)
- **1.0** — considera todos os tokens (mais diverso)
- Funciona em conjunto com a temperatura

> **Dica**: na maioria dos casos, ajuste apenas a temperatura e deixe top-p em 0.95.

## 1.3 Criando sua API Key

1. No Google AI Studio, clique em **"Get API Key"** no menu lateral
2. Clique em **"Create API Key"**
3. Selecione ou crie um projeto no Google Cloud
4. Copie a key gerada
5. **Nunca** commite a key no repositório — use `.env`

```bash
# No terminal
echo "GOOGLE_API_KEY=sua-key-aqui" > .env
```

## 1.4 Testando a API Key

```python
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explique o que é um agente de IA em uma frase."
)

print(response.text)
```

```bash
python test_api.py
```

Se obteve uma resposta, sua API Key está funcionando. Vamos para o [Bloco 2](BLOCO-2.md).
