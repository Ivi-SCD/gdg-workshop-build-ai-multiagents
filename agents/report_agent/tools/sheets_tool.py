import os
from datetime import datetime

import gspread


def _get_sheets_client():
    """Cria o cliente autenticado do Google Sheets via OAuth2 desktop flow."""
    creds_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")

    if os.path.exists(creds_file):
        return gspread.service_account(filename=creds_file)

    oauth_creds = os.getenv("GOOGLE_OAUTH_CREDENTIALS", "oauth_credentials.json")
    if os.path.exists(oauth_creds):
        return gspread.oauth(
            credentials_filename=oauth_creds,
            authorized_user_filename="authorized_user.json",
        )

    raise FileNotFoundError(
        "Nenhum arquivo de credenciais encontrado. "
        "Coloque 'oauth_credentials.json' (OAuth Client ID) ou 'credentials.json' (Service Account) na raiz do projeto."
    )


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
        recommended_allocation: Alocação recomendada de ativos.
        market_data: Dados de mercado coletados (texto formatado).
        analysis_summary: Resumo da análise e recomendações.

    Returns:
        dict com status da exportação e link da planilha.
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
            "message": f"Relatório exportado para a aba '{sheet_name}'.",
            "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}",
            "sheet_name": sheet_name,
        }
    except Exception as e:
        return {"error": f"Erro ao exportar: {str(e)}"}


def list_reports() -> dict:
    """Lista todos os relatórios existentes na planilha do Google Sheets.

    Returns:
        dict com a lista de abas/relatórios existentes na planilha.
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
            "relatorios": sheets,
            "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}",
        }
    except Exception as e:
        return {"error": f"Erro ao listar relatórios: {str(e)}"}
