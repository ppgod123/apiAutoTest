#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
from functools import partial


def chunked_file_reader(fp, block_size=1024 * 4):
    """
    生成器函数：分块读取文件内容，使用 iter 函数
    """
    # 首先使用 partial(fp.read, block_size) 构造一个新的无需参数的函数
    # 循环将不断返回 fp.read(block_size) 调用结果，直到其为 '' 时终止
    for chunk in iter(partial(fp.read, block_size), b''):
        yield chunk


def get_file_md5(fname) -> object:
    m = hashlib.md5()  # 创建md5对象
    with open(fname, 'rb') as f:
        for chunk in chunked_file_reader(f):
            m.update(chunk)  # 更新md5对象
    return m.hexdigest()  # 返回md5对象
