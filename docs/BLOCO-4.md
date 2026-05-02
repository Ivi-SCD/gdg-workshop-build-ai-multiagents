# Bloco 4 — Agente de Relatório + Google Sheets

Neste bloco vamos criar o agente que gera relatórios consolidados e exporta para Google Sheets.

## 4.1 Configurando o Google Sheets API

### Passo 1 — Criar uma Service Account

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Selecione seu projeto (ou crie um)
3. Vá em **APIs & Services > Enable APIs** e habilite **Google Sheets API** e **Google Drive API**
4. Vá em **APIs & Services > Credentials**
5. Clique em **Create Credentials > Service Account**
6. Dê um nome (ex: `workshop-sheets`)
7. Clique em **Done**
8. Clique na service account criada > **Keys > Add Key > Create new key > JSON**
9. Salve o arquivo como `credentials.json` na raiz do projeto

> **Importante**: adicione `credentials.json` ao `.gitignore` (já está lá).

### Passo 2 — Compartilhar a planilha

1. Crie uma planilha no Google Sheets
2. Compartilhe com o email da service account (encontrado no JSON, campo `client_email`)
3. Dê permissão de **Editor**

### Passo 3 — Atualizar o .env

```bash
# Adicione ao .env
GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=id-da-sua-planilha
```

O ID da planilha está na URL: `https://docs.google.com/spreadsheets/d/{ID}/edit`

## 4.2 Criando a tool de Google Sheets

```python
# tools/sheets_tool.py

import os
import json
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials


def _get_sheets_client():
    """Cria o cliente autenticado do Google Sheets."""
    creds_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
    return gspread.authorize(creds)


def export_report_to_sheets(
    report_title: str,
    investor_profile: str,
    recommended_allocation: str,
    market_data: str,
    analysis_summary: str,
) -> dict:
    """Exporta um relatório de análise de investimentos para o Google Sheets.

    Args:
        report_title: Título do relatório.
        investor_profile: Perfil do investidor (Conservador, Moderado, Arrojado, Agressivo).
        recommended_allocation: Alocação recomendada.
        market_data: Dados de mercado coletados (texto formatado).
        analysis_summary: Resumo da análise e recomendações.

    Returns:
        dict com status e link da planilha.
    """
    try:
        client = _get_sheets_client()
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")

        if not spreadsheet_id:
            return {"error": "GOOGLE_SHEETS_SPREADSHEET_ID não configurado no .env"}

        spreadsheet = client.open_by_key(spreadsheet_id)

        sheet_name = f"Relatório {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=20, cols=5)

        worksheet.update("A1:B1", [["Relatório de Investimentos", ""]])
        worksheet.update("A2:B2", [["Título", report_title]])
        worksheet.update("A3:B3", [["Data", datetime.now().strftime("%d/%m/%Y %H:%M")]])
        worksheet.update("A4:B4", [["Perfil do Investidor", investor_profile]])
        worksheet.update("A5:B5", [["Alocação Recomendada", recommended_allocation]])
        worksheet.update("A7:A7", [["Dados de Mercado"]])
        worksheet.update("A8:A8", [[market_data]])
        worksheet.update("A10:A10", [["Análise e Recomendações"]])
        worksheet.update("A11:A11", [[analysis_summary]])

        worksheet.format("A1:B1", {"textFormat": {"bold": True, "fontSize": 14}})
        worksheet.format("A2:A11", {"textFormat": {"bold": True}})

        return {
            "status": "success",
            "message": f"Relatório exportado com sucesso para a aba '{sheet_name}'.",
            "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}",
            "sheet_name": sheet_name,
        }
    except Exception as e:
        return {"error": f"Erro ao exportar para Google Sheets: {str(e)}"}


def list_reports() -> dict:
    """Lista todos os relatórios existentes na planilha do Google Sheets.

    Returns:
        dict com a lista de abas/relatórios existentes.
    """
    try:
        client = _get_sheets_client()
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")

        if not spreadsheet_id:
            return {"error": "GOOGLE_SHEETS_SPREADSHEET_ID não configurado no .env"}

        spreadsheet = client.open_by_key(spreadsheet_id)
        sheets = [ws.title for ws in spreadsheet.worksheets()]

        return {
            "total": len(sheets),
            "reports": sheets,
            "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}",
        }
    except Exception as e:
        return {"error": f"Erro ao listar relatórios: {str(e)}"}
```

## 4.3 Criando o agente de relatório

```bash
mkdir -p agents/report_agent
touch agents/report_agent/__init__.py
touch agents/report_agent/agent.py
```

```python
# agents/report_agent/agent.py

from google.adk.agents import Agent
from tools.sheets_tool import export_report_to_sheets, list_reports

report_agent = Agent(
    name="report_agent",
    model="gemini-2.0-flash",
    description="Agente que gera relatórios consolidados de investimentos e exporta para Google Sheets.",
    instruction="""
    Você é um agente especializado em gerar relatórios de investimentos.

    Seu trabalho é:
    1. Receber dados de análise (perfil do investidor, dados de mercado, recomendações)
    2. Organizar as informações de forma clara e estruturada
    3. Exportar o relatório para o Google Sheets usando a ferramenta export_report_to_sheets
    4. Listar relatórios existentes quando solicitado usando list_reports

    Ao gerar o relatório:
    - Use um título descritivo
    - Organize os dados de mercado de forma legível
    - Escreva um resumo de análise claro e acionável
    - Sempre inclua o disclaimer de que não é recomendação de investimento

    Ao final, compartilhe o link da planilha com o usuário.
    """,
    tools=[export_report_to_sheets, list_reports],
)
```

```python
# agents/report_agent/__init__.py

from .agent import report_agent

root_agent = report_agent
```

## 4.4 Testando o agente

```bash
adk web agents/
```

Teste com:
- "Gere um relatório para um investidor moderado com PETR4 a R$38,50 e dólar a R$5,20"
- "Liste os relatórios existentes"

## 4.5 Conceitos-chave aprendidos

| Conceito | Descrição |
|----------|-----------|
| Service Account | Credencial para acessar APIs Google programaticamente |
| Google Sheets API | Permite ler/escrever planilhas via código |
| Tools com side effects | Ferramentas que criam artefatos externos (planilha) |
| Formatação | O agente decide como organizar os dados antes de exportar |

No próximo bloco vamos juntar tudo com o orquestrador. Vamos para o [Bloco 5](BLOCO-5.md).
