import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pica_langchain import PicaClient, create_pica_agent
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PatientProcessor:
    def __init__(self, patient=None):
        self.patient = patient
        self.specialist_map = {
            "dengue": "Infectious Disease Specialist",
            "flu": "General Physician",
            "diabetes": "Endocrinologist",
            "cold": "General Physician"
        }
        self.load_environment()
        self.setup_pica()

        if self.patient:
            self.assign_specialist()

    def load_environment(self):
        load_dotenv()
        self.PICA_SECRET = os.getenv("PICA_SECRET")
        if not self.PICA_SECRET:
            raise Exception("PICA_SECRET not found in .env!")

    def setup_pica(self):
        self.pica_client = PicaClient(secret=self.PICA_SECRET)
        logger.info(" Number of connection definitions fetched: %d", len(self.pica_client.connection_definitions))

        self.llm = ChatOpenAI(model="gpt-3.5-turbo", api_key="dummy")

        self.agent = create_pica_agent(
            client=self.pica_client,
            llm=self.llm,
            tools=[],
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
        )

    def assign_specialist(self):
        self.specialist = self.specialist_map.get(self.patient["illness"], "General Physician")

    def send_welcome_email(self):
        prompt = (
            f"Send an email to {self.patient['email']} with subject 'Welcome to Our Hospital' and body "
            f"'Dear {self.patient['name']}, welcome! We’re here to assist with your {self.patient['illness']}.' "
            f"(Assume this uses api::gmail::v1)"
        )
        return self.agent.invoke({"input": prompt})

    def schedule_followup(self):
        prompt = (
            f"Based on '{self.patient['illness']}', suggest a follow-up visit date "
            f"(e.g., 1 month from today, {datetime.now().strftime('%Y-%m-%d')})."
        )
        response = self.agent.invoke({"input": prompt})
        followup_date = datetime.now() + timedelta(days=30)
        if "month" in response["output"].lower():
            followup_date = datetime.now() + timedelta(days=30)
        self.followup_date = followup_date
        return response

    def log_to_google_sheets(self):
        prompt = (
            f"Append to Google Sheet 'Patient_Log' with data: "
            f"{self.patient['name']}, {self.patient['illness']}, {self.specialist}, "
            f"{self.followup_date.strftime('%Y-%m-%d')} "
            f"(Assume this uses api::google-sheets::v4)"
        )
        return self.agent.invoke({"input": prompt})

    def process(self):
        try:
            email_response = self.send_welcome_email()
            followup_response = self.schedule_followup()
            sheets_response = self.log_to_google_sheets()

            print("✅ Process complete.")
            print(f"🩺 Specialist assigned: {self.specialist}")
            print(f"📅 Follow-up date: {self.followup_date.strftime('%Y-%m-%d')}")
            print(f"📧 Email response: {email_response['output']}")
            print(f"📊 Sheets response: {sheets_response['output']}")

        except Exception as e:
            print(f" Error: {str(e)}")
            raise

    def create_github_branch(self):
        """
        Creates a new branch in a GitHub repo via a Pica connection.
        """
        try:
            logger.info(" Creating GitHub branch using Pica...")

            llm = ChatOpenAI(model="gpt-4", temperature=0)
            github_agent = create_pica_agent(self.pica_client, llm)

            prompt = "Create a new branch in connection github of repository Pica and name new branch as test2"
            logger.info(" Prompt: %s", prompt)

            result = github_agent.invoke(prompt)
            logger.info(" GitHub Agent Response:\n%s", result)

        except Exception as e:
            logger.error(" Error while creating branch: %s", e)
            raise
    def check_pica_connections(self):
        try:
            logger.info(" Checking available Pica connections with gpt-4o...")

            # Reinitialize PicaClient with connector options
            client = PicaClient(
                secret=self.PICA_SECRET,
                options=PicaClientOptions(connectors=["*"])
            )

            llm = ChatOpenAI(
                temperature=0,
                model="gpt-4o",
            )

            agent = create_pica_agent(
                client=client,
                llm=llm,
                agent_type=AgentType.OPENAI_FUNCTIONS,
            )

            result = agent.invoke({
                "input": "What are the connections I have access to?"
            })

            print(f"\n Pica Connection Access Result:\n{result}")

        except Exception as e:
            logger.error(" Error checking Pica connections: %s", e)
            raise


if __name__ == "__main__":
# === Toggle between functions using comment/uncomment ===
    try:
        # --- Option 1: Process Patient Info ---
        patient_info = {
            "name": "Monish M",
            "email": "monishalur2605@gmail.com",
            "illness": "cold",
        }
        processor = PatientProcessor(patient_info)
        processor.process()

        # --- Option 2: Create GitHub Branch ---
        # processor = PatientProcessor()
        # processor.create_github_branch()

        # --- Option 3: Check Available Pica Connections ---
        # processor = PatientProcessor()
        # processor.check_pica_connections()

    except Exception as e:
        logger.error("Something went wrong: %s", e)
