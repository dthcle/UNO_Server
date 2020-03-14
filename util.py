import threading
import socket
import logging
import random
import json
import rsa
from PROTOCOL import *
from Entity import Database
from CONST import *

logging.basicConfig(level=logging.INFO)

database = Database('database.sqlite')


def response_encoder(status: str, data=None):
    """
    将即将发送给客户端的数据编码成 json 字符串
    :param status: 状态码
    :param data: 数据包
    :return: 编码完成的瞬狙
    """
    if data is None:
        data = {}
    tmp = {
        "response": status,
        "data": data
    }
    return json.dumps(tmp)


def request_parser(json_data: str):
    """
    将客户端发送的 request 请求解析为 python 对象
    :param json_data: 原 json 字符串
    :return: 解析完成的数据，包含一个 操作名称 和一组 数据
    """
    tmp = json.loads(json_data)
    protocol = tmp["request"]
    data = tmp["data"]
    return protocol, data


def return_the_full_deck():
    """
    返回一个完整的牌堆，用于初始化牌堆
    :return: 一个完整牌堆的列表
    """
    tmp_list = []
    # 添加数字卡和功能卡
    for each_color in (CARD_COLOR.RED, CARD_COLOR.BLUE, CARD_COLOR.YELLOW, CARD_COLOR.GREEN):
        tmp_list.append((each_color, CARD_CONTENT.N_0))
        for repeat in range(2):
            tmp_list.append((each_color, CARD_CONTENT.N_1))
            tmp_list.append((each_color, CARD_CONTENT.N_2))
            tmp_list.append((each_color, CARD_CONTENT.N_3))
            tmp_list.append((each_color, CARD_CONTENT.N_4))
            tmp_list.append((each_color, CARD_CONTENT.N_5))
            tmp_list.append((each_color, CARD_CONTENT.N_6))
            tmp_list.append((each_color, CARD_CONTENT.N_7))
            tmp_list.append((each_color, CARD_CONTENT.N_8))
            tmp_list.append((each_color, CARD_CONTENT.N_9))
            tmp_list.append((each_color, CARD_CONTENT.BLOCK))
            tmp_list.append((each_color, CARD_CONTENT.REVERSE))
            tmp_list.append((each_color, CARD_CONTENT.ADD2))
    # 添加万能牌
    for counter in range(4):
        tmp_list.append((CARD_COLOR.UNIVERSAL, CARD_CONTENT.CHANGE))
        tmp_list.append((CARD_COLOR.UNIVERSAL, CARD_CONTENT.ADD4))
    return tmp_list


def secret_encode(msg, encode_fun=None, key=None):
    """
    将待发送的信息加密
    :param msg: 需要加密的信息内容
    :param encode_fun: 加密算法，默认为无(None)
    :param key: 加密算法的密钥
    :return: 加密后的信息
    :rtype: bytes
    """
    tmp_msg = ''
    if not encode_fun:
        tmp_msg = msg.encode()
    elif encode_fun == RSA:
        tmp_msg = rsa.encrypt(msg, key)

    return tmp_msg


def secret_decode(msg, encode_fun=None, key=None):
    """
    将收到的加密信息解密
    :param msg: 已被加密的信息
    :param encode_fun: 解密算法
    :param key: 加密算法解密的密钥
    :return: 解密后的信息
    :rtype: str
    """
    tmp_msg = ''
    if not encode_fun:
        tmp_msg = msg.decode()
    elif encode_fun == RSA:
        tmp_msg = rsa.decrypt(msg, key)

    return tmp_msg


def match_server_get_client_request(client_socket: socket.socket, client_addr, player_dict, game_server_list, server_port_list, lock: threading.Lock):
    """
    匹配服务器接收到客户端匹配请求后回复的信息
    :param client_socket: 客户端交流的 socket
    :param client_addr: 客户端的地址、端口元组
    :param player_dict: 玩家等待列表的字典，格式参见初始化处
    :param server_port_list: 已开启游戏服务器的端口列表
    :param lock: 线程锁
    :return: None
    """
    from Entity import GameServer
    logging.info(f"get the request from client{client_addr}")
    lock.acquire()
    logging.info(f"thread locked!")

    msg = secret_decode(client_socket.recv(DATA_PACK_MAX_SIZE))
    logging.info(f"get the request content from client{client_addr}\n\t\t内容为{msg}")
    protocol, data = request_parser(msg)
    # protocol为协议类型 data为数据内容
    if protocol == MATCH_PROTOCOL:
        try:
            player_dict[data[J_PLAYER_NUM]].append((client_addr[CLIENT_ADDR_INDEX], data[J_CLIENT_PORT]))
        except KeyError:
            client_socket.send(secret_encode(response_encoder(STATUS_ALL[DATA_ERROR])))
            client_socket.close()
            return
        client_socket.send(secret_encode(response_encoder(STATUS_ALL[OK])))

        # 如果该玩家加入后人数足够开启一场游戏了 从匹配队列中移除一定玩家数 并开启一个服务器
        if len(player_dict[data[J_PLAYER_NUM]]) >= int(data[J_PLAYER_NUM]):
            player_list = player_dict[data[J_PLAYER_NUM]][:int(data[J_PLAYER_NUM])]
            player_dict[data[J_PLAYER_NUM]] = player_dict[data[J_PLAYER_NUM]][int(data[J_PLAYER_NUM]):]
            tmp_port_list = []
            for counter in range(int(data[J_PLAYER_NUM])):
                while True:
                    tmp_port = random.randint(GAME_SERVER_PORT_MIN, GAME_SERVER_PORT_MAX)
                    if tmp_port not in server_port_list:
                        tmp_port_list.append(tmp_port)
                        server_port_list.append(tmp_port)
                        break
            game_server_list.append(GameServer(int(data[J_PLAYER_NUM]), player_list, tmp_port_list))
            game_server_list[-1].run()
    if protocol == LOGIN_PROTOCOL:
        username = data[J_USERNAME]
        password = data[J_PASSWORD]
        logging.info(f"get the user info! username: {username} password: {password}")
        result = database.get_user_password(username)
        if result == NOT_FOUND or password != result:
            logging.error(f"can't find the correct user!")
            client_socket.send(secret_encode(response_encoder(STATUS_ALL[USERNAME_PASSWORD_WRONG])))
        elif result == password:
            logging.info(f"found it! username: {username}")
            # rsa_public_key = database.get_user_rsa_key(username)[0]
            # client_socket.send(secret_encode(response_encoder(STATUS_ALL[OK], {"rsa_public_key": rsa_public_key})))
            client_socket.send(secret_encode(response_encoder(STATUS_ALL[OK], {J_CLIENT_ADDR: client_addr[CLIENT_ADDR_INDEX]})))
            database.update_login_time(username)
    else:
        client_socket.send(secret_encode(response_encoder(STATUS_ALL[FORBIDDEN])))
        client_socket.close()

    lock.release()
    # # 旧版 单通过字符串进行操作
    # # INDEX
    # MATCH_PROTOCOL_OPERATION_INDEX = 0
    # MATCH_PROTOCOL_DATA_INDEX = 1
    #
    # # info 中包含 该信息的协议类型 和 该信息的内容
    # info = msg.split(DELIMITER)
    # if info[MATCH_PROTOCOL_OPERATION_INDEX] == MATCH_PROTOCOL:
    #     player_dict[info[MATCH_PROTOCOL_DATA_INDEX]].append(client_addr)
    #
    #     # 如果该玩家加入后人数足够开启一场游戏了 从匹配队列中移除一定玩家数 并开启一个服务器
    #     if len(player_dict[info[MATCH_PROTOCOL_DATA_INDEX]]) >= int(info[MATCH_PROTOCOL_DATA_INDEX]):
    #         player_list = player_dict[info[MATCH_PROTOCOL_DATA_INDEX]][:int(MATCH_PROTOCOL_DATA_INDEX)]
    #         player_dict[info[MATCH_PROTOCOL_DATA_INDEX]] = player_dict[info[MATCH_PROTOCOL_DATA_INDEX]][int(MATCH_PROTOCOL_DATA_INDEX):]
    #         tmp_port_list = []
    #         for counter in range(int(MATCH_PROTOCOL_DATA_INDEX)):
    #             while True:
    #                 tmp_port = random.randint(GAME_SERVER_PORT_MIN, GAME_SERVER_PORT_MAX)
    #                 if tmp_port not in server_port_list:
    #                     tmp_port_list.append(tmp_port)
    #                     server_port_list.append(tmp_port)
    #                     break
    #         GameServer(int(info[MATCH_PROTOCOL_DATA_INDEX]), player_list, tmp_port_list)
    # else:
    #     client_socket.send(secret_encode("Not Allowed!"))

