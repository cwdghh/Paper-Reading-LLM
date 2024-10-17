#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author             : 陈蔚 (weichen.cw@zju.edu.cn)
Date               : 2024-08-17 14:28
Last Modified By   : 陈蔚 (weichen.cw@zju.edu.cn)
Last Modified Date : 2024-10-17 13:00
Description        : This is the interface for the webapp.
-------- 
Copyright (c) 2024 Wei Chen. 
'''

import time
import os

import gradio as gr
from openai import OpenAI

from src.arguments import get_args
from src.process_file import upload_file, upload_file_from_arxiv, get_file_id
from src.query_api import query_api_webapp, convert_tuples_to_messages
from src.utils import log_history, remove_proxy
from src.config_and_variables import APP_INSTRUCTION, ENDPOINT, NO_PROXY

remove_proxy()
os.environ['no_proxy'] = NO_PROXY


log_name = None

def main():
    args = get_args()
    print(args)
    print(APP_INSTRUCTION)

    client = OpenAI(
        api_key=args.accessKey,
        base_url=ENDPOINT
    )

    def response(query, history):
        global log_name
        
        if len(history) == 0:
            # which means that we are starting a new chat
            log_name = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        
        messages = convert_tuples_to_messages(tuples=history)

        if query.startswith("arxiv:"):
            arxiv_id = query.split(":")[1]
            for i, msg in enumerate(upload_file_from_arxiv(client=client, arxiv_id=arxiv_id)):
                yield f"[STEP {i+1}/3]: {msg}"
            file_id = msg
            yield f"Finish Uploading Paper. File id: {file_id}."
            messages.append({"role": "system", "content": f"fileid://{file_id}"})
        elif query.startswith("file:"):
            file_path = query.split(":")[1].strip(':').strip("'")
            for i, msg in enumerate(upload_file(client=client, file_path=file_path)):
                yield f"[STEP {i + 1} / 2]: {msg}"
            file_id = msg
            yield f"Finish Uploading Paper. File id: {file_id}."
            messages.append({"role": "system", "content": f"fileid://{file_id}"})
        elif query.startswith("delete:"):
            file_name = query.split(":")[1].split('/')[-1]

            file_id = get_file_id(client=client, file_name=file_name)
            if file_id is not None:
                client.files.delete(file_id)
                yield f"Finish Deleting Paper. File id: {file_id}."
        else:
            for response_text in query_api_webapp(
                client=client,
                query=query,
                messages=messages
            ):
                yield response_text

        log_history(history=messages, file_name=log_name)

    chatbot = gr.Chatbot(
        height=600, 
        latex_delimiters=[
            { "left": "$$",  "right": "$$",  "display": True  },
            { "left": "$",   "right": "$",   "display": False },
            { "left": "\\(", "right": "\\)", "display": False },
            { "left": "\\[", "right": "\\]", "display": True  },
        ],
        placeholder=APP_INSTRUCTION,
    )

    gr.ChatInterface(
        response,
        chatbot=chatbot,
        textbox=gr.Textbox(lines=1, placeholder="Please Enter Your Question or Request!", container=False, scale=7),
        title="Paper Reading LLM",
        description="Ask Paper Reading LLM any question!",
        theme="soft",
        examples=["Hello, who are you?", "arxiv:2311.11100", "file:files/HowtoReadPaper.pdf", "delete:2311.11100.pdf"],
        cache_examples=False,
    ).launch()



if __name__ == '__main__':
    main()