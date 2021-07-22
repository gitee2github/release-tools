# !/usr/bin/python3
# ******************************************************************************
# Copyright (c) Huawei Technologies Co., Ltd. 2020-2020. All rights reserved.
# licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# ******************************************************************************/
"""
Logging related
"""
import logging
import os
import pathlib
from concurrent_log_handler import ConcurrentRotatingFileHandler
from javcra.libs.config.global_config import LOG_DIR


class Log(object):
    """
    operation log of the system
    """

    def __init__(self, name=__name__, path=None):
        self.__current_rotating_file_handler = None
        if not path:
            path = os.path.dirname(__file__)
        self.__path = os.path.join(path, "log_info.log")

        if not os.path.exists(self.__path):
            try:
                os.makedirs(os.path.split(self.__path)[0])
            except FileExistsError:
                pathlib.Path(self.__path).touch(mode=0o644)
        self.__max_bytes = 30000000
        self.__backup_count = 2
        self.__level = "INFO"
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(self.__level)

    def __init_handler(self):
        self.__current_rotating_file_handler = ConcurrentRotatingFileHandler(
            filename=self.__path,
            mode="a",
            maxBytes=self.__max_bytes,
            backupCount=self.__backup_count,
            encoding="utf-8",
            use_gzip=True,
        )
        self.__set_formatter()
        self.__set_handler()

    def __set_formatter(self):
        formatter = logging.Formatter(
            "%(asctime)s-%(filename)s-[line:%(lineno)d]"
            "-%(levelname)s-[ log details ]: %(message)s",
            datefmt="%a, %d %b %Y %H:%M:%S",
        )
        self.__current_rotating_file_handler.setFormatter(formatter)

    def __set_handler(self):
        self.__current_rotating_file_handler.setLevel(self.__level)
        self.__logger.addHandler(self.__current_rotating_file_handler)

    @property
    def logger(self):
        """
        Gets the logger property
        """
        if not self.__current_rotating_file_handler:
            self.__init_handler()
        return self.__logger


logger = Log(__name__, path=LOG_DIR).logger
