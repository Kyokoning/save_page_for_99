#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import inspect
import ctypes
import threading
import socket
import struct
# import struct # to send `int` as  `4 bytes`
import time
import datetime
import os, sys
import logging

logger = logging.getLogger(__name__)

def sock_service():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 创建类型为socket.SOCK_STREAM的socket对象，默认使用TCP协议
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # setsockopt(level,optname,value)
        # socket.SOL_SOCKET是正在使用的socket选项，socket.SOREUSEADDR令socket在关闭后，本地端用于该socket的端口号立刻就可以被重用。
        server.bind(('', 8082))
        # s.bind((HOST, PORT))
        # bind()用来关联socket到指定的网络接口和端口号
        # HOST可以是主机名称、IP 地址、空字符串。空字符串代表服务器将接受本机所有可用的 IPv4 地址
        # PORT应该是1-65535之间的整数（0是保留的），这个整数就是用来接收客户端连接的TCP端口号。如果端口号小于1024，可能会要求管理员权限
        server.listen(10)
        # listen()方法使服务器可以接受连接请求，成为一个监听中的socket
        # listen()有一个可选参数backlog，它指定在拒绝新的连接之前系统将允许使用的 未接受的连接数量。
        # 增加backlog参数的值可以加大等待链接请求队列的长度，最大长度取决于操作系统。
    except socket.error as msg:
        logger.info('=> socket error with meg: ', msg)
        sys.exit(1)

    logger.info('====> Waiting for connection...<====')
    while 1:
        client, addr = server.accept()
        # accept()方法阻塞并等待传入连接
        # 当一个客户端连接时，它将返回一个新的socket对象，表示当前连接的 conn 和一个由主机、端口号组成的 IPv4/v6 连接的元组
        t = threading.Thread(target=deal_data, args=(client, addr))
        t.start()


def force_close(client, number):
    time.sleep(number)
    print("Client no response, force to close connect\n===============================")
    client.close()


# _async_raise and stop_thread is for thread stopping
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

# 我们假设输入的是一串数字
def deal_data(client, addr):
    # global input_path, output_path
    time_input = datetime.datetime.now()
    logger.info('=> Accept a new connection from client: {0}, at {1}'.format(
        addr, time_input.strftime('%Y-%m-%d %H:%M:%S')))
    try:
        # get mode
        buf_type = client.recv(4)
        mode = struct.unpack("!i", buf_type)[0]
        # 0: 帖子id
        # 1：搜索tag

        # get type of the file
        buf = client.recv(4)
        # recv()的参数是缓冲区数据大小限制最大值参数，并不代表只返回这么多内容。
        word = struct.unpack("!s", buf)[0]
        # struct.unpack(format, buffer)
        # 根据字符串format从缓冲区buffer解包，结果为一个元组
        # i是大端模式（网络），s是string，i是int
        logger.info("===> Receive done, word:", word)

        record(word, mode)
        # 存贴id或者tag

        # if the client has no response in 10s, force to disconnect, and release thread.
        t1 = threading.Thread(target=force_close, args=(client, 10))
        t1.start()

        closeSignal = client.recv(1024)
        logger.info(closeSignal.decode('utf-8'))
        stop_thread(t1)
        client.close()

    except Exception as e:
        logger.info('=> threading error {} happened in client {}.'.format(e, addr))
    finally:
        logger.info("===============================")
        logger.info('Waiting for connection...')

def record(s, mode):
    # 保存的文件格式是tmp/20200916/post_id.txt
    today = time.time()-3600*12
    today = time.strftime('%Y%m%d', time.localtime(today))
    output_dir = os.path.join('temp', today)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, 'post_id.txt' if mode == 0 else 'tag.txt')
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(s+'\n')

# --- main ---
sock_service()
