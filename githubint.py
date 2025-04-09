import os
import logging
from datetime import datetime
from pica_langchain import create_pica_agent, PicaClient
from langchain_community.chat_models import ChatOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubIntegration:
    def __init__(self):
        self.pica_agent = None

    def initialize_pica_client(self):
        try:
            logger.info("Initializing Pica client...")
            secret = os.getenv("PICA_API_SECRET")
            if not secret:
                raise ValueError("Missing PICA_API_SECRET environment variable")

            client = PicaClient(secret=secret)
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            self.pica_agent = create_pica_agent(client=client, llm=llm)
            logger.info("Pica client initialized successfully.")

        except Exception as e:
            logger.error(f"Error initializing Pica client: {e}", exc_info=True)
            return False
        return True

    def create_github_branch(self):
        try:
            if not self.pica_agent:
                logger.error("Pica agent is not initialized.")
                return

            prompt = (
                "create a new branch in connection github of repository Pica "
                "and name new branch as test2"
            )

            logger.info(f"Running prompt: {prompt}")
            result = self.pica_agent.invoke(prompt)

            logger.info("=== GitHub Branch Creation Result ===")
            logger.info(result)

        except Exception as e:
            logger.error(f"Error creating GitHub branch: {e}", exc_info=True)

if __name__ == "__main__":
    github_tool = GitHubIntegration()
    if github_tool.initialize_pica_client():
        github_tool.create_github_branch()
    else:
        logger.error("Failed to initialize Pica client. Exiting.")
