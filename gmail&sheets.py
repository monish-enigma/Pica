import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pica_langchain import PicaClient

def process_patient_info(patient):
    """
    Process patient info: send welcome email, assign specialist, schedule follow-up, and log to Google Sheets.
    """
    # Assign specialist
    specialist_map = {
        "dengue": "Infectious Disease Specialist",
        "flu": "General Physician",
        "diabetes": "Endocrinologist",
    }
    specialist = specialist_map.get(patient["illness"], "General Physician")

    try:
        # Load secret from .env
        load_dotenv()
        PICA_SECRET = os.getenv("PICA_SECRET")
        if not PICA_SECRET:
            raise Exception(" PICA_SECRET not found in .env!")

        # Initialize Pica client
        pica_client = PicaClient(secret=PICA_SECRET)
        print("🔢 Number of connection definitions fetched:", len(pica_client.connection_definitions))

        # Debug available actions
        print("🔍 Gmail actions:", pica_client.get_available_actions("api::gmail::v1"))
        print("🔍 Sheets actions:", pica_client.get_available_actions("api::google-sheets::v4"))

        # Step 1: Send welcome email
        email_action = {
            "platform": "gmail",
            "key": "api::gmail::v1",
            "action": "send",  # Hypothetical; adjust from get_available_actions
            "parameters": {
                "to": patient["email"],
                "subject": "Welcome to Our Hospital",
                "body": f"Dear {patient['name']}, welcome! We’re here to assist with your {patient['illness']}."
            }
        }
        email_response = pica_client.execute(email_action)
        print(f"📧 Email response: {email_response}")

        # Step 2: Schedule follow-up (static for now)
        followup_date = datetime.now() + timedelta(days=30)

        # Step 3: Log to Google Sheets
        sheets_action = {
            "platform": "google-sheets",
            "key": "api::google-sheets::v4",
            "action": "append", 
            "parameters": {
                "sheet_name": "Patient_Log",
                "values": [patient["name"], patient["illness"], specialist, followup_date.strftime('%Y-%m-%d')]
            }
        }
        sheets_response = pica_client.execute(sheets_action)
        print(f"📊 Sheets response: {sheets_response}")

        # Step 4: Print confirmation
        print("✅ Process complete.")
        print(f"🩺 Specialist assigned: {specialist}")
        print(f"📅 Follow-up date: {followup_date.strftime('%Y-%m-%d')}")

    except Exception as e:
        print(f" Error: {str(e)}")
        print("⚠️ Falling back to simulated responses:")
        print(f"🩺 Specialist assigned: {specialist}")
        print(f"📅 Follow-up date: {(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')}")
        print("📧 Email response: Simulated email sent via api::gmail::v1")
        print("📊 Sheets response: Simulated append via api::google-sheets::v4")

# Run the app
if __name__ == "__main__":
    patient_info = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "illness": "dengue",
    }
    process_patient_info(patient_info)