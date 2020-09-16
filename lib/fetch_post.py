# -*- coding: utf-8 -*-
# @Time : 2020/9/16
# @Author : mac
# @File : fetch_post.py

import requests
import json
import os
import logging
import time
logger = logging.getLogger(__name__)

def get_post_json(post_id):
    url = 'https://www.bilibilipy.net/api/topic/{}'.format(post_id)
    topic = pre_process(url)
    if not topic:
        return -1
    page_number = 1
    page_list = []
    while(1):
        html = requests.get(url+'?page={}'.format(page_number)).text
        data = json.loads(html)
        if not data['data']['replylist']['data']: # 本页已无回复
            return topic, page_list
        page_list.append(data['data']['replylist']['data'])
        page_number += 1

def pre_process(url):
    html = requests.get(url).text
    data = json.loads(html)
    if data['code'] == 1004:
        return False # 帖子已删除
    else:
        return data['data']['topic']


def fetch_post_via_id(id_list, output_dir):
    today = time.time()-3600*8
    today = time.strftime('%Y%m%d', today)
    output_dir = os.path.join(output_dir, today)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for id in id_list:
        try:
            post = get_post_json(id)
            if post == -1:
                logger.info('=> get post back error in post id {}.'.format(id))
                continue
                # 这里可能要输出错误提示
            else:
                topic, page_list = post

                output_file = os.path.join(output_dir, topic['title']+'.md')
                res = ''
                with open(output_file, 'w', encoding = 'utf-8') as f:
                    floor = 0
                    res += 'title: ' + topic['title']+'\n\n'
                    res += 'content: ' + topic['content']+'\n'
                    res += '№'+str(floor)+' ☆☆☆ ' + topic['username'] + '于' + topic['updated_at'] + '留言☆☆☆'+'\n'

                    for page in page_list:
                        for state in page:
                            floor += 1
                            res += '-'*15+'\n'
                            res += state['content']+'\n'
                            res += '№'+str(floor)+' ☆☆☆ ' + state['username'] + '于' + state['updated_at'] + '留言☆☆☆'+'\n'
                    res += '-'*15+'\n'
                    f.write(res)

        except Exception as e:
            logger.info('=> error in post id {}.'.format(id))
