import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from orchestrator import root_agent


async def main():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="investment_advisor",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="investment_advisor",
        user_id="user",
    )

    print("=" * 50)
    print("  Sistema Multi-Agent de Investimentos")
    print("  Powered by Google ADK + Gemini")
    print("=" * 50)
    print()
    print("Agentes disponíveis:")
    print("  - Perfil de Investidor")
    print("  - RAG (Base de Conhecimento)")
    print("  - Mercado (Cotações em tempo real)")
    print("  - Relatório (Google Sheets)")
    print()
    print("Digite 'sair' para encerrar.")
    print()

    while True:
        user_input = input("Você: ").strip()

        if user_input.lower() in ("sair", "exit", "quit"):
            print("Até logo!")
            break

        if not user_input:
            continue

        message = Content(
            role="user",
            parts=[Part(text=user_input)],
        )

        response = runner.run(
            user_id="user",
            session_id=session.id,
            new_message=message,
        )

        print("\nAssistente: ", end="")
        async for event in response:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text)
        print()


if __name__ == "__main__":
    asyncio.run(main())
