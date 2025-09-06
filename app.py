import asyncio
import pprint
import os
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPClient, MCPAgent

load_dotenv()

async def main():
    """Main function to run the MCP agent with Google Generative AI."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")
    os.environ["GOOGLE_API_KEY"] = api_key

    config_file = "browser_mcp.json"

    st.title("MCP Agent")

    st.caption("initializing chat")
    client = MCPClient.from_config_file(config_file)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True
    )

    
    user_input = st.text_input("Enter your command:")
    button_clicked = st.button("Submit")
    if button_clicked:

        if user_input.lower() in ("exit", "quit"):
            print("Exiting...")


        st.caption("Processing...")
        response = await agent.run(user_input)

        print("Response:")
        pprint.pprint(response)
        st.write(response)

if __name__ == "__main__":
    asyncio.run(main())
