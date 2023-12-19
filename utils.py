import os
import time

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

thread = client.beta.threads.create()


def handle_conversation(chat_history: list) -> list[list]:
    query = chat_history[-1][0]

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=query
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=os.getenv('ASSISTANT_ID')
    )

    flag = False
    while not flag:
        retrieved_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if retrieved_run.status == 'completed':
            flag = True
        else:
            time.sleep(1.0)

    thread_messages = client.beta.threads.messages.list(thread.id)

    response = thread_messages.data[0].content[0].text.value

    chat_history[-1][1] = ""
    for character in response:
        chat_history[-1][1] += character
        time.sleep(0.01)
        yield chat_history


def handle_user_query(message: str, chat_history: list[tuple]) -> tuple:
    chat_history += [[message, None]]
    return '', chat_history
