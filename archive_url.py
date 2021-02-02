import io
import re
import uuid
import zipfile
from typing import Union

import requests
from bs4 import BeautifulSoup

MAX_FILNAME = 200
RESERVED_NAME = [
    'CON', 'PRN', 'AUX', 'NUL',
    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
]

REGEX_RESERVED_CHARACTERS = r'[\\/:*?"<>|]'
REGEX_RESERVED_NAME = rf"^({'|'.join(RESERVED_NAME)})$"


def collection_link_in_url(url: str, **kwargs) -> list:
    """
    Get list of urls to static files

    :param url: url of the site page
    :param kwargs: supported <allow_redirects> for get-request

    :return: list of links
    """

    allow_redirects = kwargs.get('allow_redirects', True)

    response = requests.get(url=url, allow_redirects=allow_redirects)
    soup_html = BeautifulSoup(response.text, features="html.parser")

    collection_link_file = [response.url]
    collection_any_tag = [
        (soup_html.find_all('link', href=True), 'href'),
        (soup_html.find_all('script', src=True), 'src'),
        (soup_html.find_all('img', src=True), 'src')
    ]

    for collection_tag, name_atrb in collection_any_tag:
        for link in collection_tag:
            if 'http' in link.attrs[name_atrb]:
                collection_link_file.append(link.attrs[name_atrb])
            else:
                collection_link_file.append(f'{response.url}{link.attrs[name_atrb][1:]}')


    return collection_link_file


def generate_filename(unique_prefix: str = '') -> str:
    """
    Generating filename

    :param unique_prefix: unique prefix for the filename (optional)

    :return: filename
    """

    return unique_prefix + str(uuid.uuid4())


def correct_filename(filename: str, unique_prefix: str = '') -> str:
    """
    Adjustment of requirements and limitations of reserved characters

    :param filename: filename for archive
    :param unique_prefix: unique prefix for filename (optional)

    :return: filename
    """

    filename = re.sub(REGEX_RESERVED_CHARACTERS, '', filename)
    filename = re.sub(REGEX_RESERVED_NAME, '', filename)

    if len(filename) == 0 or len(filename) > MAX_FILNAME:
        filename = generate_filename(unique_prefix=unique_prefix)

    return filename


def filename_in_url(url: str, default=None) -> Union[str, None]:
    """
    Find file name in url-string

    :param url: url of the site page
    :param default: standard return value if no filename

    :return: filename or <default> (see params)
    """

    index_slash = url.rfind('/')

    if index_slash == -1 or index_slash == len(url) - 1:
        return default

    return url[url.rfind('/') + 1:]


def create_zipfile(url_page: str) -> io.BytesIO:
    """
    Create archive with static files

    :param url_page: url of the site page

    :return: buffered I/O
    """

    data = io.BytesIO()

    with zipfile.ZipFile(data, 'w') as zip_fio:
        for url in collection_link_in_url(url=url_page):
            try:
                response = requests.get(url)
            except requests.ConnectionError:
                continue

            filename = filename_in_url(url, default=generate_filename(f'{url}_'))

            if response.ok:
                if 'image' in response.headers.get('Content-Type', '').lower():
                    zip_fio.writestr(correct_filename(filename), response.content)
                else:
                    zip_fio.writestr(correct_filename(filename), response.text)

    data.seek(0)

    return data
