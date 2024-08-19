#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author             : 陈蔚 (weichen.cw@zju.edu.cn)
Date               : 2024-08-17 14:28
Last Modified By   : 陈蔚 (weichen.cw@zju.edu.cn)
Last Modified Date : 2024-08-20 01:08
Description        : This is the main file for command line interface.
-------- 
Copyright (c) 2024 Wei Chen. 
'''

import time

from openai import OpenAI

from src.arguments import get_args
from src.process_file import upload_file, upload_file_from_arxiv, get_file_id
from src.query_api import query_api_command_line
from src.utils import log_history, load_log, append_message, remove_message
from src.config_and_variables import SYSTEM_PROMPT, INSTRUCTION, ENDPOINT


def main():
    args = get_args()
    print(args)
    print(INSTRUCTION)

    client = OpenAI(
        api_key=args.accessKey,
        base_url=ENDPOINT
    )
    messages = []
    append_message(messages=messages, role='system', content=SYSTEM_PROMPT)
    log_name = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    while True:
        query = input("HUMAN: ")
        file_id = None

        if query == 'Quit':
            break
        elif query == 'Clear':
            messages = []
            append_message(messages=messages, role='system', content=SYSTEM_PROMPT)

            log_name = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        elif query.startswith('arxiv:'):
            arxiv_id = query.split(':')[1]
            for i, msg in enumerate(upload_file_from_arxiv(client=client, arxiv_id=arxiv_id)):
                print(f"[STEP {i + 1}/3]: {msg}")
            file_id = msg

            append_message(messages=messages, role='system', content=f'fileid://{file_id}')

            print(f"\n=== Uploading file id: {file_id} Finished ===\n")
        elif query.startswith('file:'):
            file_path = query.split(':')[1]
            for i, msg in enumerate(upload_file(client=client, file_path=file_path)):
                print(f"[STEP {i + 1} / 2]: {msg}")
            file_id = msg
            append_message(messages=messages, role='system', content=f'fileid://{file_id}')

            print(f"\n=== Uploading file id: {file_id} Finished ===\n")
        elif query.startswith('delete:'):
            file_name = query.split(':')[1].split('/')[-1]

            file_id = get_file_id(client=client, file_name=file_name)
            if file_id is not None:
                client.files.delete(file_id)

                # remove the file in the message history.
                remove_message(messages=messages, role='system', content=f'fileid://{file_id}')
                print(f"\n=== Deleting file id: {file_id} Finished ===\n")
        elif query.startswith('load-log:'):
            log_name = query.split(':')[1]
            messages = load_log(file_name=log_name)

            print(f"\n=== Loading log: {log_name}.log Finished ===\n")
        else:
            messages = query_api_command_line(client=client, query=query, messages=messages)
            
        log_history(history=messages, file_name=log_name)



if __name__ == '__main__':
    main()