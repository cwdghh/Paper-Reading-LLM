#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author             : 陈蔚 (weichen.cw@zju.edu.cn)
Date               : 2024-08-17 14:22
Last Modified By   : 陈蔚 (weichen.cw@zju.edu.cn)
Last Modified Date : 2024-08-20 01:24
Description        : Query API through openai package.
-------- 
Copyright (c) 2024 Wei Chen. 
'''

import re
from typing import Generator, Any, List

from openai import OpenAI

from src.config_and_variables import MODEL_TYPE, SYSTEM_PROMPT
from src.utils import append_message, remove_message


def query_api_command_line(client: OpenAI = None, query: str = None, messages: List[dict] = None) -> List[dict]:
    """Query API through openai package in command line.

    Parameters
    ----------
    client : OpenAI, optional
        client used, by default None
    query : str, optional
        query to the LLM, by default None
    messages : List[dict], optional
        messages in the history, by default None

    Returns
    -------
    List[dict]
        messages after the query
    """
    append_message(messages, role='user', content=query)

    completion = client.chat.completions.create(
        model=MODEL_TYPE,
        messages=messages,
        stream=True
    )

    print("\n=== Model Response Start ===\n")
    response_text = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].model_dump()['delta']['content'], end="", flush=True)
            response_text += chunk.choices[0].model_dump()['delta']['content']
    print("\n\n=== Model Response End ===\n")

    append_message(messages, role='assistant', content=response_text)
    return messages


def query_api_webapp(client: OpenAI = None, query: str = None, messages: List[dict] = None) -> Generator[Any, Any, Any]:
    """Query API through openai package in Web APP.

    Parameters
    ----------
    client : OpenAI, optional
        client used, by default None
    query : str, optional
        query to the LLM, by default None
    messages : List[dict], optional
        messages in the history, by default None

    Yields
    ------
    Generator[Any, Any, Any]
        messages after the query
    """
    append_message(messages, role='user', content=query)

    completion = client.chat.completions.create(
        model=MODEL_TYPE,
        messages=messages,
        stream=True
    )

    print("\n=== Model Response Start ===\n")
    response_text = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].model_dump()['delta']['content'], end="", flush=True)
            response_text += chunk.choices[0].model_dump()['delta']['content']
            yield response_text
    print("\n\n=== Model Response End ===\n")

    append_message(messages, role='assistant', content=response_text)


def convert_tuples_to_messages(tuples: List[tuple] = None) -> List[dict]:
    """Convert history tuples to messages in OpenAI format.

    Parameters
    ----------
    tuples : List[tuple], optional
        tuples of history, consists of (user_input, assistant_response), by default None

    Returns
    -------
    List[dict]
        messages in OpenAI format
    """
    messages = []
    append_message(messages, role='system', content=SYSTEM_PROMPT)

    for user, assistant in tuples:
        if user.startswith('arxiv:') or user.startswith('file:'):

            match = re.search(r'File id: ([\w-]+)', assistant)
            if match:
                file_id = match.group(1)
                append_message(messages, role='system', content=f'fileid://{file_id}')

        elif user.startswith('delete:'):

            match = re.search(r'File id: ([\w-]+)', assistant)
            if match:
                file_id = match.group(1)
                remove_message(messages, role='system', content=f'fileid://{file_id}')
            
        else:

            append_message(messages, role='user', content=user)
            append_message(messages, role='assistant', content=assistant)

    return messages
