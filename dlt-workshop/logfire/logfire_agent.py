import logfire
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv(override=True)

logfire.configure()
logfire.instrument_pydantic_ai()

agent = Agent('openai:gpt-5.2')

while True:
    prompt = input()

    if prompt.lower() == "exit":
        break

    result = agent.run_sync(prompt)

    print(f'OUTPUT:\n{result}')
    print("========================================")