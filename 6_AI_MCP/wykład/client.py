from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage

load_dotenv()

server_params = StdioServerParameters(
    command="python3",
    # Full absolute path to the server.py file
    args=["server.py"],
)
# Uwaga: export OPENAI_API_KEY=sk-proj-1234567890

import asyncio

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)

            agent = create_agent('openai:gpt-4o-mini', tools=tools)
            agent_response = await agent.ainvoke({"messages": [HumanMessage(content="What's (3 + 5) x 12?")]})
            print(agent_response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())