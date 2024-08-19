#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author             : 陈蔚 (weichen.cw@zju.edu.cn)
Date               : 2024-08-17 14:23
Last Modified By   : 陈蔚 (weichen.cw@zju.edu.cn)
Last Modified Date : 2024-08-20 01:08
Description        : Configuration and global variables.
-------- 
Copyright (c) 2024 Wei Chen. 
'''

# 1. Proxy Configuration

HTTP_PROXY  = "http://127.0.0.1:1087"       # HTTP proxy
ALL_PROXY   = "http://127.0.0.1:1086"       # All proxy
NO_PROXY    = "localhost, 127.0.0.1, ::1"   # No proxy, no need to be changed. You should set no proxy to use the proxy with Gradio

# 2. Global Variables

FILE_DIR        = "files"       # Temporary directory to store files
LOG_DIR         = "logs"        # Log directory
ENDPOINT        = "https://dashscope.aliyuncs.com/compatible-mode/v1"   # Endpoint
MODEL_TYPE      = "qwen-long"   # Model type
SYSTEM_PROMPT   = "You are an expert in the field of deep learning research."
INSTRUCTION     = r"""
=== Instruction ===
Chat with LLM about papers!

1. Input 'Q' to exit / Input 'C' to clear history.
2. Input 'arxiv:<arxiv_paper_id>', e.g. 'arxiv:2311.11100', to download and chat about the paper.
3. Input 'file:<your_file_path>', e.g. 'file:files/HowtoReadPaper.pdf', to upload and chat about the paper.
4. Input 'delete:<arxiv_paper_id/file_name>', e.g. 'delete:2311.11100.pdf' or 'delete:HowtoReadPaper.pdf', to delete the paper.
5. Input 'load-log:<file_name>' , e.g. 'load-log:2024-08-19_15-56-26', to load the chat history.
6. It may take a while to download/upload the paper.

=== Instruction End ===
"""

# 3. Gradio Configuration

LATEX_DELIMITERS    = [
    { "left": "$$",  "right": "$$",  "display": True  },
    { "left": "$",   "right": "$",   "display": False },
    { "left": "\\(", "right": "\\)", "display": False },
    { "left": "\\[", "right": "\\]", "display": True  },
]   # LaTeX delimiters

APP_TITLE       = "Paper Reading LLM"
APP_DESCRIPTION = "Ask Paper Reading LLM any question!\n\nYou could specify a paper using Arxiv Id in format 'arxiv:2402.14700'. It may take a while to download the paper."
APP_INSTRUCTION = r"""
<strong>Your Personal Paper Reading LLM!</strong>

<div style="text-align:left; line-height: 2;">
Ask the Paper Reading LLM any question! Here are some instructions that might be helpful:

<ol>
<li>You could specify a paper using arxiv id in format 'arxiv:<arxiv_id>', e.g. 'arxiv:2311.11100'.</li>
<li>You could specify a local paper using file path in format 'file:<your_file_path>', e.g. 'file:files/HowtoReadPaper.pdf'.</li>
<li>You could delete a paper using file name in the format 'delete:<arxiv_id/file_name>', e.g. 'delete:2311.11100.pdf' or 'delete:HowtoReadPaper.pdf'.</li>
<li>It may take a while to download/upload the paper.</li>
</ol>
</div>"""
