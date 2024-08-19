#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author             : 陈蔚 (weichen.cw@zju.edu.cn)
Date               : 2024-08-17 14:46
Last Modified By   : 陈蔚 (weichen.cw@zju.edu.cn)
Last Modified Date : 2024-08-20 01:31
Description        : Arugments
-------- 
Copyright (c) 2024 Wei Chen. 
'''

import argparse
from argparse import Namespace

from src.config_and_variables import HTTP_PROXY, ALL_PROXY, NO_PROXY


def get_args() -> Namespace:
    """Parse and return the arguments of the program.

    Returns
    -------
    Namespace
        arguments of the program
    """
    parser = argparse.ArgumentParser(description='Paper Reading LLM Arguments.')
    parser.add_argument('--accessKey', '-a', type=str, default=None, help='DashScope API Key')
    parser.add_argument('--useProxy',  '-p', action='store_true', help='Use proxy')

    args = parser.parse_args()

    assert args.accessKey is not None, 'Please set your DashScope API Key.'

    if not args.useProxy:
        global HTTP_PROXY, ALL_PROXY, NO_PROXY

        print('No proxy is used.')
        HTTP_PROXY  = ''
        ALL_PROXY   = ''
        NO_PROXY    = ''

    return args