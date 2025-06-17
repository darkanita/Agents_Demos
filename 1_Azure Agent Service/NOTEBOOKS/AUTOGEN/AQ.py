# AQ.py - Exported from 1_AUTOGEN-with-Azure_AI_Agents_team.ipynb

# Cell 1
#%pip install azure-ai-projects

# Cell 2
# Example of using three Azure AI agents with AUTOGEN as the orchestrator

# Cell 3
from PIL import Image
from pathlib import Path
from IPython.display import display, HTML
import os
import sys
import time

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from azure.ai.agents import AgentsClient 
from azure.ai.agents.models import CodeInterpreterTool, BingGroundingTool
import os
import yaml

from dotenv import load_dotenv
load_dotenv()

from azure.identity import DefaultAzureCredential

# Cell 4
with open("/Users/arturoquiroga/GITHUB/AZURE AI AGENT SERVICE/1_Azure Agent Service/NOTEBOOKS/AUTOGEN/model_config.yaml", "r") as f:
    model_config = yaml.safe_load(f)
model_client = AzureOpenAIChatCompletionClient.load_component(model_config)

# Cell 5
endpoint = os.getenv("PROJECT_ENDPOINT")
print(f"Using endpoint: {endpoint}")
credential = DefaultAzureCredential()

project_client = AgentsClient(endpoint=endpoint, credential=credential)

# Cell 6
project_client = AgentsClient(
    credential=DefaultAzureCredential(),
    endpoint=endpoint
)

# Cell 7
# [START create_agent_with_bing_grounding_tool]
conn_id = os.getenv("AZURE_BING_CONNECTION_ID")

# Initialize agent bing tool and add the connection id
bing = BingGroundingTool(connection_id=conn_id)

# Cell 8
# define the web_ai_agent, with BING grounding
async def web_ai_agent(query: str) -> str:
    print()
    print("This is Bing for Azure AI Agent Service .......")
    print()
    bing = BingGroundingTool(connection_id=conn_id)
    agent = project_client.create_agent(
        model="gpt-4.1-mini",
        name="my-web-agent",
        instructions="""
            You are a web search agent.
            Your only tool is search_tool - use it to find information.
            You make only one search call at a time.
            Once you have the results, you never do calculations based on them.
        """,
        tools=bing.definitions,
        headers={"x-ms-enable-preview": "true"}
    )
    print(f"Created agent, ID: {agent.id}")

    thread = project_client.threads.create()
    print(f"Created thread, ID: {thread.id}")

    message = project_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=query,
    )
    print(f"SMS: {message}")

    run = project_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    project_client.delete_agent(agent.id)
    print("Deleted agent")

    messages_paged = project_client.messages.list(thread_id=thread.id)
    messages = list(messages_paged)
    if messages:
        print("Messages:" + messages[0]["content"][0]["text"]["value"])
        return messages[0]["content"][0]["text"]["value"]
    else:
        print("No messages found.")
        return ""

# Cell 9
# Define the blog writer agent with Code Interpreter tool
from IPython.display import FileLink

async def save_blog_agent(blog_content: str) -> str:
    print()
    print("This is Code Interpreter for Azure AI Agent Service .......")

    code_interpreter = CodeInterpreterTool()
    agent = project_client.create_agent(
        model="gpt-4.1-mini",
        name="my-coder-agent",
        instructions="You are helpful agent",
        tools=code_interpreter.definitions,
    )

    thread = project_client.threads.create()

    message = project_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"""
            You are my Python programming assistant. Generate code, save the following blog content, and execute it according to the requirements:

            {blog_content}

            1. Save blog content to blog-Agentic_AI_Blog.md
            2. Give me the download link for this file.
        """,
    )

    run = project_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    messages_paged = project_client.messages.list(thread_id=thread.id)
    messages = list(messages_paged)
    if messages:
        print("Messages:" + messages[0]["content"][0]["text"]["value"])
    else:
        print("No messages found.")

    # Save the file to a notebook-accessible directory
    file_name = f"AI_Blog_{time.strftime('%Y%m%d%H%M%S')}.md"
    target_dir = "./blog"
    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(blog_content)
    print(f"File saved: {file_path}")

    # Display a download link in the notebook
    display(FileLink(file_path, result_html_prefix="Download your blog: "))

    project_client.delete_agent(agent.id)
    print("Deleted agent")

    return "Saved"

# Cell 10
# Define the three agents
bing_search_agent = AssistantAgent(
    name="bing_search_agent",
    model_client=model_client,
    tools=[web_ai_agent],
    system_message="You are a search expert, help me use tools to find relevant knowledge",
)

save_blog_content_agent = AssistantAgent(
    name="save_blog_content_agent",
    model_client=model_client,
    tools=[save_blog_agent],
    system_message="""
        Save blog content. Respond with 'Saved' to when the blog is saved.
    """
)

write_agent = AssistantAgent(
    name="write_agent",
    model_client=model_client,
    system_message="""
        You are a blog writer, please help me write a blog based on bing search content."
    """
)

# Cell 11
text_termination = TextMentionTermination("Saved")
# Define a termination condition that stops the task after 5 messages.
max_message_termination = MaxMessageTermination(10)
# Combine the termination conditions using the `|` operator so that the
# task stops when either condition is met.
termination = text_termination | max_message_termination

# Cell 12
# Define the AUTOGEN team of Azure AI agents
reflection_team = RoundRobinGroupChat([bing_search_agent, write_agent, save_blog_content_agent], termination_condition=termination)

# Cell 13
# start the team chat
# Example usage:
# await Console(
#     reflection_team.run_stream(task="""
#         I am writing one blog about machine learning. 
#         Search for the following 3 questions and write a blog based on the search results ,
#         save it, and give me the download this file link
#         1. What is Machine Learning?
#         2. The difference between AI and ML
#         3. The history of Machine Learning
#         4. The future of Machine Learning
#     """)
# )  # Stream the messages to the console.

# Cell 14
# await Console(
#     reflection_team.run_stream(task="""
#         I am writing one blog about agentic AI. 
#         Search for the following 3 questions and write a blog based on the search results ,
#         save it, and give me the download this file link
#         1. What is Agentic AI?
#         2. The difference between AI and Agentic AI
#         3. The history of Agentic AI
#         4. The future of Agentic AI
#     """)
# )  # Stream the messages to the console.

# Cell 15
# If not installed, uncomment the next line:
# %pip install gradio

