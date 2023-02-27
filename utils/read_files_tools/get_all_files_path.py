#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2022/3/28 13:22
"""
import os


def get_all_files(file_path, yaml_data_switch=False) -> list:
    """
    获取文件路径
    :param file_path: 目录路径
    :param yaml_data_switch: 是否过滤文件为 yaml格式， True则过滤
    :return:
    """
    filename = []
    # 获取所有文件下的子文件名称
    for root, dirs, files in os.walk(file_path):
        for _file_path in files:
            path = os.path.join(root, _file_path)
            if yaml_data_switch:
                if 'yaml' in path or '.yml' in path:
                    filename.append(path)
            else:
                filename.append(path)
    return filename


def clear_empty_dir(dir_path: str) -> None:
    for root, dirs, files in os.walk(dir_path, topdown=False):
        if not files and not dirs:
            os.rmdir(root)


if __name__ == "__main__":
    from common.setting import ensure_path_sep
    a = get_all_files(ensure_path_sep("\\data"), yaml_data_switch=True)
    print(a)