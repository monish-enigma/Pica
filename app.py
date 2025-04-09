import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pica_langchain import PicaClient, create_pica_agent
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI

def process_patient_info(patient):
    """
    Process patient info: send welcome email, assign specialist, schedule follow-up, and log to Google Sheets.
    """
    try:
        # Load secret from .env
        load_dotenv()
        PICA_SECRET = os.getenv("PICA_SECRET")
        if not PICA_SECRET:
            raise Exception(" PICA_SECRET not found in .env!")

        # Initialize Pica client
        pica_client = PicaClient(secret=PICA_SECRET)
        print("🔢 Number of connection definitions fetched:", len(pica_client.connection_definitions))

        # Get LLM (hope Pica proxies it)
        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key="dummy")

        # Create agent without tools to test LLM
        agent = create_pica_agent(
            client=pica_client,
            llm=llm,
            tools=[],  # Temporarily disable tools
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
        )

        # Assign specialist
        specialist_map = {
            "dengue": "Infectious Disease Specialist",
            "flu": "General Physician",
            "diabetes": "Endocrinologist",
        }
        specialist = specialist_map.get(patient["illness"], "General Physician")

        # Step 1: Send welcome email (as text instruction)
        email_prompt = (
            f"Send an email to {patient['email']} with subject 'Welcome to Our Hospital' and body "
            f"'Dear {patient['name']}, welcome! We’re here to assist with your {patient['illness']}.' "
            f"(Assume this uses api::gmail::v1)"
        )
        email_response = agent.invoke({"input": email_prompt})

        # Step 2: Schedule follow-up with LLM
        followup_prompt = (
            f"Based on '{patient['illness']}', suggest a follow-up visit date "
            f"(e.g., 1 month from today, {datetime.now().strftime('%Y-%m-%d')})."
        )
        followup_response = agent.invoke({"input": followup_prompt})
        followup_date = datetime.now() + timedelta(days=30)  # Fallback
        if "month" in followup_response["output"].lower():
            followup_date = datetime.now() + timedelta(days=30)

        # Step 3: Log to Google Sheets (as text instruction)
        sheets_prompt = (
            f"Append to Google Sheet 'Patient_Log' with data: "
            f"{patient['name']}, {patient['illness']}, {specialist}, {followup_date.strftime('%Y-%m-%d')} "
            f"(Assume this uses api::google-sheets::v4)"
        )
        sheets_response = agent.invoke({"input": sheets_prompt})

        # Step 4: Print confirmation
        print("✅ Process complete.")
        print(f"🩺 Specialist assigned: {specialist}")
        print(f"📅 Follow-up date: {followup_date.strftime('%Y-%m-%d')}")
        print(f"📧 Email response: {email_response['output']}")
        print(f"📊 Sheets response: {sheets_response['output']}")

    except Exception as e:
        print(f" Error: {str(e)}")
        raise

# Run the app
if __name__ == "__main__":
    patient_info = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "illness": "dengue",
    }
    process_patient_info(patient_info)
