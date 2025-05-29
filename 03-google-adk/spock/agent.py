import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


os.environ["OPENAI_API_KEY"] = "tada"
os.environ["OPENAI_API_BASE"] = f"{os.environ.get('DMR_BASE_URL')}/engines/llama.cpp/v1"

def say_hello(name: str):
    """
    A tool that says hello to someone.
    """
    return f"Hello, {name}! 👋"

def vulcan_salute(name: str):
    """
    A tool that greets someone with a Vulcan salute.
    """
    return f"Live long and prosper, {name}! 🖖"


root_agent = Agent(
    model=LiteLlm(model="openai/ai/qwen2.5:latest"),
    name="spock_agent",
    description=(
        """
        Spock agent that can say hello to someone or greet them with a Vulcan salute.
        It can also answer questions about the Star Trek universe.
        """
    ),
    instruction="""
    You are Spock, a Vulcan science officer. 
    You are logical and precise in your responses. 
    Use the tools provided to interact with users.
    You can say hello to someone or greet them with a Vulcan salute.
    You can also answer questions about the Star Trek universe.
    """,
    tools=[
        say_hello,
        vulcan_salute
    ],

)


