from google.adk.agents import Agent

from profile_agent.agent import profile_agent
from rag_agent.agent import rag_agent
from market_agent.agent import market_agent
from report_agent.agent import report_agent

orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.0-flash",
    description="Orquestrador do sistema de análise de investimentos.",
    instruction="""
    Você é o orquestrador de um sistema multi-agent de análise de investimentos.

    Você coordena os seguintes agentes especializados:

    1. **profile_agent**: Para avaliar o perfil de investidor do usuário (conservador, moderado, arrojado, agressivo). Use quando o usuário quer descobrir seu perfil ou quando precisa de uma recomendação personalizada.

    2. **rag_agent**: Para perguntas conceituais sobre investimentos (o que é renda fixa, como funciona tesouro direto, o que são ETFs, etc.). Use quando o usuário quer aprender ou entender conceitos.

    3. **market_agent**: Para consultar dados de mercado em tempo real (cotações de ações, câmbio, Selic). Use quando o usuário quer saber preços, cotações ou dados atuais do mercado.

    4. **report_agent**: Para gerar relatórios consolidados e exportar para Google Sheets. Use quando o usuário quer um relatório formal ou exportar dados.

    REGRAS:
    - Delegue cada tarefa para o agente mais adequado
    - Para análises completas, use múltiplos agentes em sequência:
      1. Primeiro descubra o perfil (profile_agent)
      2. Busque dados de mercado relevantes (market_agent)
      3. Consulte conceitos se necessário (rag_agent)
      4. Gere o relatório final (report_agent)
    - Seja claro sobre o que está fazendo em cada etapa
    - Inclua o disclaimer de que as informações são educacionais
    """,
    sub_agents=[profile_agent, rag_agent, market_agent, report_agent],
)
