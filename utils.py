import time
import re

import config
from logger import values_bot_logger


def handle_conversation(chat_history: list, query: str = None, isUI: bool = True, thread_id: str = '') -> list[list]:

    if thread_id == '':
        thread = config.client.beta.threads.create()
    else:
        thread = config.client.beta.threads.retrieve(thread_id=thread_id)

    if query == None:
        query = chat_history[-1][0]

    config.client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=query
    )
    run = config.client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=config.ASSISTANT_ID
    )

    flag = False
    while not flag:
        retrieved_run = config.client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if retrieved_run.status == 'completed':
            flag = True
        else:
            time.sleep(1.0)

    thread_messages = config.client.beta.threads.messages.list(thread.id)

    response = thread_messages.data[0].content[0].text.value

    response = re.sub(r"【\d+†source】", "", response)

    values_bot_logger.info(f'Response -> {response}')

    if isUI:
        chat_history[-1][1] = response
        return chat_history
    else:
        return response, thread.id


def handle_user_query(message: str, chat_history: list[tuple]) -> tuple:
    chat_history += [[message, None]]
    return '', chat_history
