# 🏥 Hospital Enlisting and Welcome Mail Service (Pica-based Integration)

This prototype for hospital user enlistment and automated email services, built using Pica and other modern tools. I first connected github to Pica in the website and used chat feature to create new branch or commit/PR or sending a mail, after which I used the SDKs to do the same programatically. The application captures user details and performs the following:

- Stores submitted data into **Google Sheets** via **Pica**.
- Sends a **welcome email** to the user via pica.
- Creates new branch from code level
---

## 🧩 Features
Needs these variables to run: 
export PICA_SECRET="your-pica-secret"
export OPENAI_API_KEY="your-openai-api-key"
## ✨ Features

| Feature                          | Description |
|----------------------------------|-------------|
| 📧 Welcome Emails                | Automatically sends a welcome email to new patients via Gmail (through Pica). |
| 🧠 AI-based Follow-up Scheduling | Suggests follow-up dates based on the patient's illness using OpenAI. |
| 📊 Google Sheets Integration     | Appends patient data to Google Sheets for record keeping. |
| 🔧 GitHub Automation             | Creates a GitHub branch programmatically for dev workflow tasks. |
| 🔍 Connection Introspection      | Lists all connected Pica services and APIs available to the agent. |

---

## 🛠️ Tech Stack

- **LangChain** – for agent orchestration
- **Pica SDK** – to integrate with cloud APIs using natural language
- **OpenAI GPT** – for email drafting, scheduling logic, and decision-making
- **Google APIs** – Gmail and Sheets via Pica
- **GitHub API** – for branch management
- **PostgreSQL** – (optional) fallback patient data storage

---
