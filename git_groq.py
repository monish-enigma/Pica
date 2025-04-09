import logging
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from pica_langchain.client import PicaClient
from pica_langchain.agent import create_pica_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Initializing Pica client...")
        client = PicaClient(secret="sk_test_1_tbfgndlE763_cWpxa5SD144IDyATdUaRXNqq4MZEDFQiWqrPHkTXxiMdYYoC0j6uneKOKUwH-Er83ivKAjyITaHX634VyTy16U4VTeu20GMq9GAOv6zK0PbAYf-RUq8EIridOiSHnE6g70SeozeUAXL6xKrFw8U1wDGrCATzKlAeaHzHv0XoP5a_2_C1U8Nq0WSCmO0YfFiEOYYjGQ2P3PZfZJesE_p_Ez5Zr2ljWQ")

        llm = ChatGroq(
            groq_api_key="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",
            model_name="phi-3-mini-128k-instruct"
        )

        agent_executor = create_pica_agent(client, llm=llm)

        prompt = "Create a new branch in connection github of repository Pica and name new branch as test-groq"
        logger.info("Running prompt: %s", prompt)

        result = agent_executor.run(prompt)
        print("\n🔧 RESULT:")
        print(result)

    except Exception as e:
        logger.error(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()
