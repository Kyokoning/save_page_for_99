# -*- coding: utf-8 -*-
# @Time : 2020/9/16
# @Author : xnchen
# @File : launcher.py

from yacs.config import CfgNode as CN
import time, os

_C = CN()

_C.OUTPUT_DIR = 'output/'
_C.LOG_DIR = 'log/'

_C.KEYWORD = True
_C.KEYWORD_LIST = []

_C.POST = True
_C.POST_LIST = []

cfg = _C

def update_config(cfg, args):
    cfg.defrost()
    cfg.merge_from_file(args.cfg)
    wait_list = today_list()
    cfg.merge_from_list(wait_list)
    cfg.freeze()

def today_list():
    wait_list = []
    today = time.strftime('%Y%m%d')
    for target_txt, MODE in zip(['tag.txt', 'post_id.txt'], ['KEYWORD', 'POST']):
        file = os.path.join('temp', today, target_txt)
        if os.path.exists(file):
            target_list = []
            with open(file, 'r') as f:
                for line in f.readlines():
                    if line:
                        target_list.append(line.strip())
            if target_list:
                wait_list.append(MODE)
                wait_list.append(True)
                wait_list.append(MODE+'_LIST')
                wait_list.append(target_list)
    return wait_list

if __name__ == '__main__':
    print(_C)