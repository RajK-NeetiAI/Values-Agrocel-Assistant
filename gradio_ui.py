import gradio as gr

from utils import *
import config
from logger import values_bot_logger

with gr.Blocks(
    css='footer {visibility: hidden}'
) as demo:

    thread_id = config.client.beta.threads.create().id
    values_bot_logger.info(thread_id)
    temp_text_box = gr.Textbox(value=thread_id, visible=False)

    chatbot = gr.Chatbot(
        label='Talk to Values Assistant', bubble_full_width=False)
    msg = gr.Textbox(label='Query', placeholder='Enter text and press enter')
    clear = gr.ClearButton([msg, chatbot], variant='stop')

    msg.submit(
        handle_user_query,
        [msg, chatbot],
        [msg, chatbot]
    ).then(
        handle_conversation,
        [chatbot, temp_text_box],
        [chatbot]
    )

demo.queue()
