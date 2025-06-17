# AQgradio.py - Gradio interface for AQ.py

import gradio as gr
import asyncio
from AQ import reflection_team

# Define a synchronous wrapper for the async team chat
def agent_team_chat(user_message):
    async def run_team():
        result = await reflection_team.run(task=user_message)
        # If result is a list of message objects, extract the text content
        if isinstance(result, list):
            # Only extract the 'content' field from each message
            texts = []
            for msg in result:
                # If msg has a 'content' attribute, use it; otherwise, convert to string
                content = getattr(msg, "content", None)
                if content:
                    texts.append(str(content))
            return "\n\n".join(texts)
        return str(result)
    return asyncio.run(run_team())

with gr.Blocks() as demo:
    gr.Markdown("# Azure AI Agent Team Chat")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Enter your question here and then click Send", placeholder="Type your message here...   ")
    send_btn = gr.Button("Send")

    def respond(history, user_message):
        response = agent_team_chat(user_message)
        history = history or []
        history.append((user_message, response))
        return history, ""

    send_btn.click(respond, [chatbot, msg], [chatbot, msg])

demo.launch()
