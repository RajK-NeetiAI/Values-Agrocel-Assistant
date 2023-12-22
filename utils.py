import time
import re

from openai import OpenAI

import config


client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

thread = client.beta.threads.create()


def handle_conversation(chat_history: list, query: str = None, isUI: bool = True) -> list[list]:
    if query == None:
        query = chat_history[-1][0]

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=query
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=config.ASSISTANT_ID
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

    response = re.sub(r"【\d+†source】", "", response)

    if isUI:
        chat_history[-1][1] = response
        return chat_history
    else:
        return response


def handle_user_query(message: str, chat_history: list[tuple]) -> tuple:
    chat_history += [[message, None]]
    return '', chat_history
