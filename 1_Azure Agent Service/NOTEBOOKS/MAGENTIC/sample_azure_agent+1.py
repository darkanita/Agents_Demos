# sample_azure_agent+1.py - Updated for Azure AI Agents SDK (azure.ai.agents)
"""
This script demonstrates how to use the new Azure AI Agents SDK to create an agent, send a message, and print the response.
Set the environment variables PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME before running.
"""
import asyncio
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.agents.azure._azure_ai_agent import AzureAIAgent
import dotenv
import os
from typing import Union, Any, Dict, Optional
from autogen_core.models import ChatCompletionClient
from autogen_core import ComponentModel
from autogen_agentchat.agents import UserProxyAgent

from magentic_ui.tools.playwright.browser import get_browser_resource_config
from magentic_ui.utils import get_internal_urls
from magentic_ui.teams import GroupChat, RoundRobinGroupChat
from magentic_ui.teams.orchestrator.orchestrator_config import OrchestratorConfig
from magentic_ui.agents import WebSurfer, CoderAgent, USER_PROXY_DESCRIPTION, FileSurfer
from magentic_ui.magentic_ui_config import MagenticUIConfig, ModelClientConfigs
from magentic_ui.types import RunPaths
from magentic_ui.agents.web_surfer import WebSurferConfig
from magentic_ui.agents.users import DummyUserProxy, MetadataUserProxy
from magentic_ui.approval_guard import (
    ApprovalGuard,
    ApprovalGuardContext,
    ApprovalConfig,
    BaseApprovalGuard,
)
from magentic_ui.input_func import InputFuncType, make_agentchat_input_func
from magentic_ui.learning.memory_provider import MemoryControllerProvider


import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
dotenv.load_dotenv()

import dotenv


def main():
    endpoint = os.environ["PROJECT_ENDPOINT"]
    deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]

    agents_client = AgentsClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )

    with agents_client:
        # Create an agent
        agent = agents_client.create_agent(
            model=deployment_name,
            name="azure_agent",
            instructions="You are a helpful assistant."
        )
        print(f"Created agent, agent ID: {agent.id}")

        # Create a thread
        thread = agents_client.threads.create()
        print(f"Created thread, thread ID: {thread.id}")

        # Send a message
        message = agents_client.messages.create(
            thread_id=thread.id,
            role="user",
            content="How are you doing?"
        )
        print(f"Created message, message ID: {message.id}")

        # Run the agent
        run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
        print(f"Run completed with status: {run.status}")

        # Fetch and print all messages
        messages = agents_client.messages.list(thread_id=thread.id)
        for msg in messages:
            print(f"{msg.role}: {getattr(msg, 'content', getattr(msg, 'text', ''))}")

        # Delete the agent when done
        agents_client.delete_agent(agent.id)
        print("Deleted agent")

if __name__ == "__main__":
    main()
