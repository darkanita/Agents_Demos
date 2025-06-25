import os
from azure.ai.agents import AgentsClient 
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool, FilePurpose, ListSortOrder, BingGroundingTool, MessageRole
from azure.identity import DefaultAzureCredential
import streamlit.components.v1 as components
import streamlit as st
from PIL import Image
from dotenv import load_dotenv  
load_dotenv()



# Set page config
st.set_page_config(
    page_title = "Agent Service - Demo Kit",
    page_icon = ":ninja:",
    layout = "wide"
)

# Initialise key UI Demo Kit variables
project_connstring = os.getenv("PROJECT_ENDPOINT")
gpt_model = os.getenv("MODEL_DEPLOYMENT_NAME")
bing_search = os.getenv("AZURE_BING_CONNECTION_ID")

# Set sidebar navigation
st.sidebar.title("Instructions:")
st.sidebar.markdown(
    """
    This Streamlit app is a UI Demo Kit for Azure AI Foundry's Agent Service.

    For source code, setup instructions and more details, visit the [GitHub repo](https://github.com/LazaUK/AIFoundry-AgentService-Streamlit).
    """
)
menu = st.sidebar.radio("Choose a capability:", ("Code Interpreter", "Bing Search"))

# Helper Function for Code Interpreter capability
def code_interpreter(prompt, conn_str=project_connstring, model=gpt_model):
    st.session_state["interpreter_image"] = ""
    st.session_state["interpreter_code"] = ""

    try:
        # Initiate AI Project client
        project_client = AgentsClient.create_agent(
            credential = DefaultAzureCredential(),
            conn_str = conn_str
        )
        progress_bar = st.progress(0)
        st.session_state.progress += 25
        progress_bar.progress(st.session_state.progress)

        # Add Code Interpreter to the Agent's ToolSet
        code_interpreter = CodeInterpreterTool()

        # Initiate Agent Service
        agent = project_client.agents.create_agent(
            model = model,
            name = "code-interpreter-agent",
            instructions = "You are a helpful data analyst. You can use Python to perform required calculations.",
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
        )
        print(f"Created agent, agent ID: {agent.id}")
        st.session_state.progress += 25
        progress_bar.progress(st.session_state.progress)

        # Create a thread
        thread = project_client.threads.create()
        print(f"Created thread, thread ID: {thread.id}")
        st.session_state.progress += 25
        progress_bar.progress(st.session_state.progress)

        # Create a message
        message = project_client.messages.create(
            thread_id = thread.id,
            role = "user",
            content = prompt
        )
        print(f"Created message, message ID: {message.id}")

        # Run the agent
        run = project_client.runs.create_and_process(
            thread_id = thread.id,
            assistant_id = agent.id
        )

        # Check the run status
        if run.status == "failed":
            project_client.delete_agent(agent.id)
            print(f"Deleted agent, agent ID: {agent.id}")
            progress_bar.empty()
            return f"Run failed: {run.last_error}"

        # Get the last message from the agent
        messages = project_client.list_messages(thread_id=thread.id)
        last_msg = messages.get_last_text_message_by_sender("assistant")
        result = last_msg.text.value if last_msg else "No response from agent."

        # Retrieve the image file
        if messages.file_path_annotations:
            file_path_annotation = messages.file_path_annotations[0]
            file_name = f"interpreter_image_file.png"
            project_client.agents.save_file(
                file_id = file_path_annotation.file_path.file_id,
                file_name = file_name
            )
            print(f"Downloaded image, file name: {file_name}")
            st.session_state['interpreter_image'] = file_name
            st.session_state.progress += 25
            progress_bar.progress(st.session_state.progress)

        # Retrieve the Python code snippet
        run_details = project_client.agents.list_run_steps(
            thread_id = thread.id,
            run_id = run.id
        )
        for steps in run_details.data:
            if getattr(steps.step_details, 'type', None) == "tool_calls":
                for calls in steps.step_details.tool_calls:
                    input_value = getattr(calls.code_interpreter, 'input', None)
                    if input_value:
                        print("Extracted Python code snippet")
                        st.session_state['interpreter_code'] = input_value

        # Delete the agent once done
        project_client.agents.delete_agent(agent.id)
        print(f"Deleted agent, agent ID: {agent.id}")
        progress_bar.empty()

        return result

    except Exception as e:
        progress_bar.empty()
        st.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"

# Helper Function for Bing Search capability
def bing_search(prompt, conn_str=project_connstring, model=gpt_model, connection_name=bing_search):
    try:
        # Initialize AI Project client
        project_client = AIProjectClient.from_connection_string(
            credential = DefaultAzureCredential(),
            conn_str = conn_str
        )
        progress_bar = st.progress(0)
        st.session_state.progress += 25
        progress_bar.progress(st.session_state.progress)

        # Initialize Bing Grounding Tool
        bing_connection = project_client.connections.get(
            connection_name = connection_name
        )
        connection_id = bing_connection.id
        bing = BingGroundingTool(connection_id=connection_id)

        # Initiate Agent Service
        agent = project_client.agents.create_agent(
            model = model,
            name = "bing-search-agent",
            instructions = "You are a helpful assistant that uses Bing Search to answer user questions.",
            tools = bing.definitions,
            headers={"x-ms-enable-preview": "true"}
        )
        print(f"Created agent, agent ID: {agent.id}")
        st.session_state.progress += 25
        progress_bar.progress(st.session_state.progress)

        # Create a thread
        thread = project_client.agents.create_thread()
        print(f"Created thread, thread ID: {thread.id}")
        st.session_state.progress += 25
        progress_bar.progress(st.session_state.progress)

        # Create a message
        message = project_client.agents.create_message(
            thread_id = thread.id,
            role = "user",
            content = prompt
        )
        print(f"Created message, message ID: {message.id}")

        # Run the agent
        run = project_client.agents.create_and_process_run(
            thread_id = thread.id,
            assistant_id = agent.id
        )

        # Check the run status
        if run.status == "failed":
            project_client.agents.delete_agent(agent.id)
            print(f"Deleted agent, agent ID: {agent.id}")
            progress_bar.empty()
            return f"Run failed: {run.last_error}", ""

        # Retrieve messages from the agent
        messages = project_client.agents.list_messages(thread_id=thread.id)
        result = ""
        citations = []
        for message in messages.data:
            if message.role == "assistant":
                result = message.content[0].text.value                
                for annotation in message.content[0].text.annotations:
                    citation_text = annotation.text
                    citation_url = annotation['url_citation']['url']
                    citations.append(f"{citation_text}: {citation_url}")
                print("Retrieved groundings from Bing Search")
                st.session_state.progress += 25
                progress_bar.progress(st.session_state.progress)

        # Delete the agent once done
        project_client.agents.delete_agent(agent.id)
        print(f"Deleted agent, agent ID: {agent.id}")
        progress_bar.empty()
        
        result = result if result else "No response from agent."
        return result, citations

    except Exception as e:
        progress_bar.empty()
        st.error(f"An error occurred: {e}")
        return f"An error occurred: {e}", ""

# Main screen
st.title("Azure AI Foundry's Agent Service Demo Kit")

if menu == "Code Interpreter":
    st.header("Solving challenging problems with sandboxed Python code")
    default_prompt = "Could you please analyse the operating profit of Contoso Inc. using the following data and producing a bar chart image. Contoso Inc. Operating Profit: Quarter 1: $2.2 million, Quarter 2: $2.5 million, Quarter 3: $2.3 million, Quarter 4: $3.8 million, Industry Average: $2.5 million. When quarter values in 2024 fall below the industry average, please highlight them in red, otherwise they should be green."
    prompt = st.text_area("Enter your prompt:", value=default_prompt, height=150)
    if st.button("Run"):
        st.session_state.progress = 0
        result = code_interpreter(prompt)
        st.text_area("Output:", value=str(result), height=200)
        if st.session_state.get('interpreter_image'):
            img = Image.open(st.session_state['interpreter_image'])
            st.image(img, caption="Image generated by Code Interpreter")
        if st.session_state.get('interpreter_code'):
            st.text_area("Python Code Snippet:", value=st.session_state['interpreter_code'], height=300)
    if st.button("Clear"):
        st.text_area("Output:", value="", height=200)
        st.session_state['interpreter_image'] = ''
        st.session_state['interpreter_code'] = ''

elif menu == "Bing Search":
    st.header("Grounding output with real-time Bing Search results")
    default_prompt = "Can you provide a summary of the 2024 Formula 1 season, including the key highlights. I need 3 paragraphs to describe the season."
    prompt = st.text_area("Enter your search query:", value=default_prompt, height=150)
    if st.button("Run"):
        st.session_state.progress = 0
        result, citations = bing_search(prompt)
        st.markdown(result, unsafe_allow_html=True)
        if citations:
            st.markdown("### Citations")
            for citation in citations:
                st.markdown(f"- {citation}")
    if st.button("Clear"):
        pass

else:
    st.header("Please, choose a capability from the sidebar.")