from google.adk.agents.llm_agent import Agent

# Ferramenta para classificar o perfil do investidor com base nas respostas do usuário.
def classify_profile(
    risk_tolerance: str,
    investment_horizon: str,
    experience: str,
    objective: str,
) -> dict:
    """Classifica o perfil do investidor com base nas respostas do usuário.

    Args:
        risk_tolerance: Tolerância a risco (baixa, media, alta).
        investment_horizon: Horizonte de investimento (curto, medio, longo).
        experience: Experiência com investimentos (nenhuma, pouca, moderada, muita).
        objective: Objetivo principal (preservar_capital, renda, crescimento, especulacao).

    Returns:
        dict com o perfil classificado e recomendações de alocação.
    """
    score = 0

    risk_scores = {"baixa": 1, "media": 2, "alta": 3}
    horizon_scores = {"curto": 1, "medio": 2, "longo": 3}
    experience_scores = {"nenhuma": 1, "pouca": 1, "moderada": 2, "muita": 3}
    objective_scores = {
        "preservar_capital": 1,
        "renda": 2,
        "crescimento": 3,
        "especulacao": 4,
    }

    score += risk_scores.get(risk_tolerance, 2)
    score += horizon_scores.get(investment_horizon, 2)
    score += experience_scores.get(experience, 1)
    score += objective_scores.get(objective, 2)

    if score <= 5:
        profile = "Conservador"
        allocation = "80% Renda Fixa, 15% Fundos Multimercado, 5% Renda Variável"
    elif score <= 8:
        profile = "Moderado"
        allocation = "50% Renda Fixa, 25% Fundos Multimercado, 25% Renda Variável"
    elif score <= 11:
        profile = "Arrojado"
        allocation = "25% Renda Fixa, 25% Fundos Multimercado, 50% Renda Variável"
    else:
        profile = "Agressivo"
        allocation = "10% Renda Fixa, 20% Fundos Multimercado, 70% Renda Variável"

    return {
        "perfil": profile,
        "score": score,
        "alocacao_recomendada": allocation,
        "tolerancia_risco": risk_tolerance,
        "horizonte": investment_horizon,
    }

# Definição do agente de perfil de investidor
profile_agent = Agent(
    name="profile_agent",
    model="gemini-2.5-flash",
    description="Agente que avalia o perfil de investidor do usuário através de perguntas.",
    instruction="""
    Você é um agente especializado em avaliação de perfil de investidor.

    Seu trabalho é fazer perguntas ao usuário para entender:
    1. Tolerância a risco (baixa, media, alta)
    2. Horizonte de investimento (curto: até 1 ano, medio: 1-5 anos, longo: 5+ anos)
    3. Experiência com investimentos (nenhuma, pouca, moderada, muita)
    4. Objetivo principal (preservar_capital, renda, crescimento, especulacao)

    Faça as perguntas de forma conversacional e amigável, uma de cada vez.
    Quando tiver todas as respostas, use a ferramenta classify_profile para classificar.
    Apresente o resultado de forma clara e explique o que cada perfil significa.
    Sempre mencione que a análise é educacional e não constitui recomendação de investimento.
    """,
    tools=[classify_profile],
)