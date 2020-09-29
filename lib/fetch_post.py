# -*- coding: utf-8 -*-
# @Time : 2020/9/16
# @Author : mac
# @File : fetch_post.py

import requests
import json
import os, time
import logging

logger = logging.getLogger(__name__)


def get_post_json (post_id):
    url = 'https://www.bilibilipy.net/api/topic/{}'.format(post_id)
    print(url)
    topic = pre_process(url)
    if not topic:
        return -1
    page_number = 1
    page_list = []
    while (1):
        html = requests.get(url + '?page={}'.format(page_number)).text
        data = json.loads(html)
        if not data['data']['replylist']['data']:  # 本页已无回复
            return topic, page_list
        page_list.append(data['data']['replylist']['data'])
        page_number += 1


def pre_process (url):
    html = requests.get(url).text
    data = json.loads(html)
    if data['code'] == 1004:
        return False  # 帖子已删除
    else:
        return data['data']['topic']

def fetch_post_via_id (id_list, output_dir):
    for id in id_list:
        try:
            post = get_post_json(id)
            if post == -1:
                logger.info('=> get post back error in post id {}.'.format(id))
                continue
                # 这里可能要输出错误提示
            else:
                topic, page_list = post

                output_file = os.path.join(output_dir, topic['title'][:50] + '.md')
                res = ''
                with open(output_file, 'w', encoding = 'utf-8') as f:
                    floor = 0
                    res += 'title: ' + topic['title'] + '\n\n'
                    res += 'content: ' + topic['content'] + '\n'
                    res += '№' + str(floor) + ' ☆☆☆ ' + topic['username'] + '于' + topic['updated_at'] + '留言☆☆☆' + '\n'

                    for page in page_list:
                        for state in page:
                            floor += 1
                            res += '-' * 15 + '\n\n'
                            content = state['content'].strip().split('<br/>')
                            for c in content[:-1]:
                                res += '    ' + c + '\n'
                            res += content[-1] + '\n\n'
                            res += '№' + str(floor) + ' ☆☆☆ ' + state['username'] + '于' + state[
                                'updated_at'] + '留言☆☆☆' + '\n'
                    res += '-' * 15 + '\n\n'
                    f.write(res)

        except Exception as e:
            logger.info('=> error {} in post id {}.'.format(e, id))

def fetch_post_via_tag_list(tag_list, output_dir):
    for tag in tag_list:
        fetch_post_via_tag(tag, output_dir)

def fetch_post_via_tag (tag, output_dir):
    post_id_list = get_search_post_id(tag)
    logger.info("=> tag: {}; post_id_list: {};".format(tag, post_id_list))
    fetch_post_via_id(post_id_list, output_dir)

def get_search_post_id (tag):
    if not tag:
        return
    url = "https://www.bilibilipy.net/search?type=1&fid=914&&pagesize=30&key="\
          +quote_unicode(tag)
    page = 0
    post_id_list = []
    stop = False
    while(not stop):
        search_html = requests.get(
            url+"&page="+str(page)
        ).text
        search_data = json.loads(search_html)
        if not search_data["code"]==200 or not search_data["data"]["docs"]:
            break
        for post in search_data["data"]["docs"]:
            if not valid_post(post["created_at"]):
                stop = True
                break
            else:
                logger.info("=> fetch tag = "+tag+", id = "+post["id"]+", title = "+post["title"])
                post_id_list.append(post["id"])
        page += 1
    return post_id_list


def valid_post(time_str):
    # 99的时间戳是这么写的：2020-09-28T09:13:15Z
    post_time = time.mktime(time.strptime(time_str,
                                          '%Y-%m-%d{}%H:%M:%S{}'.format('T', "Z")))
    day_time = day_time = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(time.time())), "%Y-%m-%d")))
    if int(time.strftime('%H'))>=8:
        if post_time>=day_time+8*2400:
            return True
        else:
            return False
    else:
        if post_time<day_time+8*2400:
            return True
        else:
            return False

def quote_unicode(str):
    return requests.utils.quote(str)