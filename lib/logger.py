# -*- coding: utf-8 -*-
# @Time : 2020/9/16
# @Author : mac
# @File : logger.py
import logging
import time
import os

def create_logger(cfg):
    time_str = str(time.strftime('%Y-%m-%d'))
    log_file_name = '{}.log'.format(time_str)

    if not os.path.exists(cfg.OUTPUT_DIR):
        os.makedirs(cfg.OUTPUT_DIR)
    log_file_path = os.path.join(cfg.LOG_DIR, log_file_name)
    head = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename = log_file_path,
                        format = head)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logging.getLogger('').addHandler(console)

    return logger, log_file_path