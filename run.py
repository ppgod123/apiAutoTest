#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/29 15:01

import os
import sys
import traceback
import pytest

from utils.other_tools.models import NotificationType
from utils.other_tools.allure_data.allure_report_data import AllureFileClean
from utils.logging_tool.log_control import INFO
from utils.notify.ding_talk import DingTalkSendMsg
from utils.notify.send_mail import SendEmail
from utils.other_tools.allure_data.error_case_excel import ErrorCaseExcel
from utils import config
from utils.read_files_tools.case_automatic_control import TestCaseAutomaticGeneration
from variable import system


def run():
    # 从配置文件中获取项目名称
    try:
        INFO.logger.info(
            """
                             _    _         _      _____         _
              __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
             / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
            | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
             \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
                  |_|
                  开始执行{}项目...
                """.format(config.project_name)
        )

        # 更新生成test_case下的文件内容
        TestCaseAutomaticGeneration(system_name=system).get_case_automatic()

        pytest.main(['-s', f'./test_case/{system}', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                     '--alluredir', './report/tmp', "--clean-alluredir"])

        """
        --reruns: 失败重跑次数
        --count: 重复执行次数
        -v: 显示错误位置以及错误的详细信息
        -s: 等价于 pytest --capture=no 可以捕获print函数的输出
        -q: 简化输出信息
        -m: 运行指定标签的测试用例
        -x: 一旦错误，则停止运行
        --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
        "--reruns=3", "--reruns-delay=2"
        """

        os.system(r"allure generate ./report/tmp -o ./report/html --clean")

        allure_data = AllureFileClean().get_case_count()
        notification_mapping = {
            NotificationType.DING_TALK.value: DingTalkSendMsg(allure_data).send_ding_notification,
            NotificationType.EMAIL.value: SendEmail(allure_data).send_main,
        }

        if config.notification_type != NotificationType.DEFAULT.value:
            notification_mapping.get(config.notification_type)()
        if config.excel_report:
            ErrorCaseExcel().write_case()

        if config.allure_open_switch:
            os.system(f"allure serve ./report/tmp -h 127.0.0.1 -p 9999")

    except Exception:
        e = traceback.format_exc()
        # 如有异常，相关异常有需要发送邮件
        if config.email.switch:
            send_email = SendEmail(AllureFileClean.get_case_count())
            send_email.error_mail(e)
        raise


if __name__ == '__main__':
    run()