import gradio as gr

from utils import *

with gr.Blocks(
    css='footer {visibility: hidden}'
) as demo:

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
        [chatbot],
        [chatbot]
    )

demo.queue()
