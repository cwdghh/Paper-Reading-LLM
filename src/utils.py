#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author             : 陈蔚 (weichen.cw@zju.edu.cn)
Date               : 2024-08-17 14:24
Last Modified By   : 陈蔚 (weichen.cw@zju.edu.cn)
Last Modified Date : 2024-10-17 11:49
Description        : Utils for the project.
-------- 
Copyright (c) 2024 Wei Chen. 
'''

import json
import os
from contextlib import contextmanager
from typing import Generator, List

from src.config_and_variables import LOG_DIR, USE_PROXY, HTTP_PROXY, ALL_PROXY, NO_PROXY


@contextmanager
def proxy_context() -> Generator[None, None, None]:
    """Context manager to set/unset proxy environment variables.

    Yields
    ------
    Generator[None, None, None]
        Enter/Exist context.
    """
    try:
        if USE_PROXY:
            print('Setting proxy...')
            os.environ['http_proxy']    = HTTP_PROXY
            os.environ['https_proxy']   = HTTP_PROXY
            os.environ['all_proxy']     = ALL_PROXY
            os.environ['no_proxy']      = NO_PROXY
        else:
            print('Not setting proxy...')
        yield
    finally:
        if USE_PROXY:
            print('Unsetting proxy...')
            del os.environ['http_proxy']
            del os.environ['https_proxy']
            del os.environ['all_proxy']
            del os.environ['no_proxy']


def remove_proxy() -> None:
    # Remove proxy first, please specify in `src/config_and_variables.py` if needed.
    if 'http_proxy' in os.environ:
        del os.environ['http_proxy']
    
    if 'https_proxy' in os.environ:
        del os.environ['https_proxy']

    if 'all_proxy' in os.environ:
        del os.environ['all_proxy']

    if 'ALL_PROXY' in os.environ:
        del os.environ['ALL_PROXY']
        
    if 'no_proxy' in os.environ:
        del os.environ['no_proxy']


def append_message(messages: List[dict], role: str = None, content: str = None) -> None:
    """Append a message to the messages list.

    Parameters
    ----------
    messages : List[dict]
        messages list to be appended.
    role : str, optional
        role of the message, by default None
    content : str, optional
        content of the message, by default None
    """
    if role != 'system':
        messages.append({
            'role': role,
            'content': content
        })
    else:
        need_to_append = True
        for message in messages:
            if message['role'] == 'system' and message['content'] == content:
                need_to_append = False
        if need_to_append:
            messages.append({
                'role': role,
                'content': content
            })


def remove_message(messages: List[dict], role: str = None, content: str = None) -> None:
    """Remove a message from the messages list.

    Parameters
    ----------
    messages : List[dict]
        messages list to be removed.
    role : str, optional
        role of the message, by default None
    content : str, optional
        content of the message, by default None
    """
    delete_index = []
    for i, message in enumerate(reversed(messages)):
        if message['role'] == role and message['content'] == content:
            delete_index.append(len(messages) - 1 - i)

    for index in delete_index:
        messages.pop(index)

def log_history(history: List[dict], file_name: str = None) -> None:
    """Log the history to a file.

    Parameters
    ----------
    history : List[dict]
        history to be logged.
    file_name : str, optional
        file name, by default None
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    if file_name is None:
        file_name = 'default_log'

    file_path = os.path.join(LOG_DIR, f"{file_name}.log")
    
    with open(file_path, 'w') as f:
        f.write(json.dumps(history, ensure_ascii=False, indent=4))


def load_log(file_name: str = None) -> List[dict]:
    """Load the log from a file.

    Parameters
    ----------
    file_name : str, optional
        file name, by default None

    Returns
    -------
    List[dict]
        messages list loaded.
    """
    if file_name is None:
        file_name = 'default_log'

    file_path = os.path.join(LOG_DIR, f"{file_name}.log")

    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r') as f:
        history = json.load(f)

    return history