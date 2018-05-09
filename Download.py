"""
带进度下载文件方法
"""

import os
from urllib.request import urlopen

import requests

# python进度库
from tqdm import tqdm


def download_from_url(url, dst):
    """
    @param: url to download file
    @param: dst place to put the file
    """

    file_size = int(urlopen(url).info().get('Content-Length', -1))
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


DOWNLOAD_URL = "http://www.feicuiz.com/weixin/Upload/ueditor/video/20171228/5a446a8230d5f.mp4"
DIR = "./"

if __name__ == '__main__':
    str = DOWNLOAD_URL.split('/')
    fileName = str[len(str) - 1]
    download_from_url(DOWNLOAD_URL, DIR + fileName)
