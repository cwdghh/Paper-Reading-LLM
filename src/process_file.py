#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author             : 陈蔚 (weichen.cw@zju.edu.cn)
Date               : 2024-08-17 14:21
Last Modified By   : 陈蔚 (weichen.cw@zju.edu.cn)
Last Modified Date : 2024-09-22 19:33
Description        : Download, process and upload the file.
-------- 
Copyright (c) 2024 Wei Chen. 
'''

import os
import urllib.request as libreq
from pathlib import Path
from typing import Generator, Any
from urllib.parse import urlencode

import feedparser
from openai import OpenAI

from src.config_and_variables import FILE_DIR
from src.utils import proxy_context


def download_file(link_href: str = None, file_path: str = None) -> str:
    """Download file from link and save to file path.

    Parameters
    ----------
    link_href : str, optional
        hyper link to download the file, by default None
    file_path : str, optional
        path to store the file, by default None

    Returns
    -------
    str
        path to the file.
    """
    with proxy_context():
        os.system(f"curl {link_href} --output {file_path}")
    
    return file_path


def upload_file(client: OpenAI = None, file_path: str = None) -> Generator[Any, Any, Any]:
    """Upload file through OpenAI API.

    Parameters
    ----------
    client : OpenAI, optional
        client used, by default None
    file_path : str, optional
        path to the file to be uploaded, by default None

    Yields
    ------
    Generator[Any, Any, Any]
        output messages

    Raises
    ------
    FileNotFoundError
        raised when file not found
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    
    file_name = os.path.basename(file_path)

    # Upload file if not exists
    should_upload = True
    for file in client.files.list().data:
        if file.filename == file_name:
            yield f"File {file_name} already exists, skip uploading..."
            file_id = file.id
            should_upload = False
            break

    if should_upload:
        yield f"Uploading file {file_name}..."
        file_object = client.files.create(file=Path(file_path), purpose="file-extract")
        file_id = file_object.id

    yield file_id


def get_file_id(client: OpenAI = None, file_name: str = None) -> str:
    """Get file id from OpenAI API.

    Parameters
    ----------
    client : OpenAI, optional
        client used, by default None
    file_name : str, optional
        name of the file, by default None

    Returns
    -------
    str
        File id of the file
    """
    file_id = None
    for file in client.files.list().data:
        if file.filename == file_name:
            file_id = file.id
            break

    if file_id is None:
        print(f"File {file_name} not found...")
    else:
        print(f"File {file_name}. File id: {file_id}...")

    return file_id


def query_arxiv_api(search_query: str = None) -> dict:
    """Query ArXiv API.

    Parameters
    ----------
    search_query : str, optional
        query used, by default None

    Returns
    -------
    dict
        parsed response from ArXiv API
    """
    # Modified from https://info.arxiv.org/help/api/examples/python_arXiv_parsing_example.txt
    # I adapt the code to Python 3.

    # Base api query url
    base_url = 'http://export.arxiv.org/api/query?'

    # Search parameters
    # sortBy = 'submittedDate'
    sortBy = 'relevance'
    sortOrder = 'descending'
    start = 0                     # retreive the first results
    max_results = 1

    data = {
        "search_query": search_query,
        "sortBy": sortBy,
        "sortOrder": sortOrder,
        "start": start,
        "max_results": max_results
    }

    # perform a GET request using the base_url and query
    print("Searching url: " + base_url + urlencode(data))

    with libreq.urlopen(base_url + urlencode(data)) as url:
        response = url.read()

    # parse the response using feedparser
    feed = feedparser.parse(response)

    # Run through each entry, and print out information
    # for entry in feed.entries:
    if len(feed.entries) <= 0:
        print(f"Haven't found paper for search query: {search_query}, continue...")
        exit(0)

    return feed


def query_arxiv_keyword(keyword: str = None) -> dict:
    """Query ArXiv API by keyword.

    Parameters
    ----------
    keyword : str, optional
        keywords to be queried, by default None

    Returns
    -------
    dict
        parsed response from ArXiv API
    """
    search_query = f'all:{keyword.lower()}' # search for id in all fields
    feed = query_arxiv_api(search_query=search_query)

    return feed


def query_arxiv_id_list(id_list: str = None) -> dict:
    """Query ArXiv API by id list.

    Parameters
    ----------
    id_list : str, optional
        id list to be queried, by default None

    Returns
    -------
    dict
        parsed response from ArXiv API
    """
    search_query = f'id_list="{id_list}"' # search for id in all fields
    feed = query_arxiv_api(search_query=search_query)

    return feed

def upload_file_from_arxiv(client: OpenAI = None, arxiv_id: str = None) -> Generator[Any, Any, Any]:
    """Upload file queried from ArXiv API.

    Parameters
    ----------
    client : OpenAI, optional
        client used, by default None
    arxiv_id : str, optional
        arxiv id of the paper to be download/upload, by default None

    Yields
    ------
    Generator[Any, Any, Any]
        message to be displayed
    """
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)

    file_path = os.path.join(FILE_DIR, f"{arxiv_id}.pdf")

    if not os.path.exists(file_path):
        feed = query_arxiv_id_list(id_list=arxiv_id)
        links = feed.entries[0].links

        for link in links:
            if link.type == 'application/pdf':
                yield f"Downloading paper {arxiv_id} from {link.href}..."
                download_file(link_href=link.href, file_path=file_path)
                break
    else:
        yield f"File {file_path} already exists, skip downloading..."

    for msg in upload_file(client=client, file_path=file_path):
        yield msg
