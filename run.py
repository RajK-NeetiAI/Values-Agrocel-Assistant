import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from gradio_ui import demo
from utils import handle_conversation
import config
from logger import values_bot_logger

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return 'Gradio UI is running at /gradio', 200


class ValuesChatRequest(BaseModel):
    query: str
    chat_history: list[list]
    thread_id: str | None


@app.post('/values/chat')
def values_chat(values_chat_request: ValuesChatRequest):
    query = values_chat_request.query
    chat_history = values_chat_request.chat_history
    thread_id = values_chat_request.thread_id
    values_bot_logger.info('New request came...')
    values_bot_logger.info(values_chat_request)
    try:
        response, thread_id = handle_conversation(
            chat_history, query, False, thread_id)
        values_bot_logger.info(response)
        values_bot_logger.info(thread_id)
        return {
            'status': 1,
            'response': response,
            'thread_id': thread_id
        }
    except Exception as e:
        values_bot_logger.exception(e)
        return {
            'status': 0,
            'response': config.ERROR_MESSAGE,
            'thread_id': ''
        }


app = gr.mount_gradio_app(app, demo, '/gradio')
