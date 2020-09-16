# -*- coding: utf-8 -*-
# @Time : 2020/9/16
# @Author : xnchen
# @File : launcher.py

import _init_paths
from lib.config import cfg
from lib.config import update_config
import argparse, os, time, shutil
from lib.logger import create_logger
from lib.fetch_post import fetch_post_via_id

def parse_args():
    parser = argparse.ArgumentParser(description = 'Train setting')

    parser.add_argument('--cfg',
                        help = 'configure file name',
                        required = True, type = str)  # 命令行里包含config文件位置

    args = parser.parse_args()
    return args

def gc(dir_list):
    # 删除距离如今时间有3天的log文件和temp文件
    current_time = time.time()
    tmp_dir = 'temp/'
    log_dir = cfg.LOG_DIR
    for day_dir in os.listdir(tmp_dir):
        dir_path = os.path.join(tmp_dir, day_dir)
        create_time = os.path.getctime(dir_path)
        if (current_time - create_time) // (24 * 3600) >= 3:
            shutil.rmtree(dir_path)
    for log_file in os.listdir(log_dir):
        log_path = os.path.join(log_dir, log_file)
        create_time = os.path.getctime(log_path)
        if (current_time - create_time) // (24 * 3600) >= 3:
            os.remove(log_path)

if __name__ == '__main__':
    args = parse_args()
    update_config(cfg, args)
    logger, _ = create_logger(cfg)
    logger.info(cfg)

    gc()

    if cfg.POST:
        fetch_post_via_id(cfg.POST_LIST, cfg.OUTPUT_DIR)


