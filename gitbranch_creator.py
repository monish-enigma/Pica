# hitting pica but gpt4

import os
import logging
from pica_langchain import create_pica_agent, PicaClient
from langchain_openai import ChatOpenAI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_branch():
    # Step 1: Read secret from environment
    secret = os.getenv("PICA_SECRET")
    if not secret:
        raise ValueError("PICA_SECRET environment variable is not set.")

    # Step 2: Create Pica client with secret
    logger.info("Initializing Pica client...")
    client = PicaClient(secret=secret)

    # Step 3: Setup LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # Step 4: Create agent
    pica_agent = create_pica_agent(client, llm)

    # Step 5: Define prompt
    prompt = "Create a new branch in connection github of repository Pica and name new branch as test2"
    logger.info(f"Running prompt: {prompt}")

    # Step 6: Run agent
    result = pica_agent.invoke(prompt)
    logger.info("Agent response:\n%s", result)

if __name__ == "__main__":
    try:
        create_branch()
    except Exception as e:
        logger.error("Something went wrong: %s", e)
