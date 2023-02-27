#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2022/4/25 20:02
# @File    : testcase_template
# @describe: 用例模板
"""

import datetime


def write_case(case_path, page):
    """ 写入用例数据 """
    with open(case_path, 'w', encoding="utf-8") as file:
        file.write(page)


def write_testcase_file(*, allure_epic, allure_feature, class_title,
                        func_title, case_path, case_ids, file_name, allure_story):
    """

        :param allure_story:
        :param file_name: 文件名称
        :param allure_epic: 项目名称
        :param allure_feature: 模块名称
        :param class_title: 类名称
        :param func_title: 函数名称
        :param case_path: case 路径
        :param case_ids: 用例ID
        :return:
        """
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    page = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : {now}


import allure
import pytest
from utils.read_files_tools.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.requests_tool.request_control import RequestControl
from utils.read_files_tools.regular_control import regular
from utils.requests_tool.teardown_control import TearDownHandler


case_id = {case_ids}
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


@allure.epic("{allure_epic}")
@allure.feature("{allure_feature}")
class Test{class_title}:

    @allure.story("{allure_story}")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_{func_title}(self, in_data, case_skip):
        """
        :param :
        :return:
        """
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data['assert_data']).assert_equality(response_data=res.response_data,
                                                       sql_data=res.sql_data, status_code=res.status_code)


if __name__ == '__main__':
    pytest.main(['{file_name}', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
'''
    write_case(case_path=case_path, page=page)
