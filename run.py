import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from gradio_ui import demo
from utils import handle_conversation
import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return 'Gradio UI is running at /gradio', 200


class ValuesChatRequest(BaseModel):
    query: str
    chat_history: list[list]


@app.post('/values/chat')
def values_chat(values_chat_request: ValuesChatRequest):
    query = values_chat_request.query
    chat_history = values_chat_request.chat_history
    try:
        response = handle_conversation(chat_history, query, False)
        print(response)
        return {
            'status': 1,
            'response': response
        }
    except:
        return {
            'status': 0,
            'response': config.ERROR_MESSAGE
        }


app = gr.mount_gradio_app(app, demo, '/gradio')
