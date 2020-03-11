import random
import logging
import socket
import sqlite3
import time
import hashlib
import base64
import rsa
import os
from util import *
from CONST import *
from pprint import pprint

logging.basicConfig(level=logging.INFO)


class GameServer:
    """
    服务器一直开一个服务端等待连接，客户端发送玩家IP和期望游戏的玩家数来请求连接
    服务器接收到后加入等待玩家列表，人数满足后直接新建GameServer进行游戏
    """
    def __init__(self, player_number: int, player_list: list, port: list):
        logging.info(f"启动游戏服务器.....")
        self.socket_list = []
        for each_ip in player_list:
            # 需要每个客户机上开启一个服务端
            socket_tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_list.append(socket_tmp)


class Client:
    def __init__(self, username):
        self.username = username
        self.public_key, self.private_key = database.get_user_rsa_key(username)

    def __str__(self):
        return self.username


class MatchServer:
    """
    匹配服务器，一般启动一台
    """
    def __init__(self, server_addr, server_port):
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_socket.bind((server_addr, server_port))
        self.main_socket.listen(5)


class RSACrypto:
    """
    RSA加密解密的封装类
    """
    def __init__(self):
        pass

    @staticmethod
    def encrypt(msg: str, pub_key, max_length=117):
        """
        通过公钥加密消息，并用base64将其编码成可见字符
        :param msg: 字符串消息明文
        :type: str
        :param pub_key: 公钥
        :param max_length: 最大一次加密长度(超过则进行分段加密)
        :return: 被base64编码后的密文
        :rtype: bytes
        """
        if len(msg) <= max_length:
            return base64.b64encode(rsa.encrypt(msg.encode(), pub_key))
        else:
            tmp_result = b''
            while msg:
                tmp_msg = msg[:max_length]
                msg = msg[max_length:]
                tmp_result += rsa.encrypt(tmp_msg.encode(), pub_key)
            return base64.b64encode(tmp_result)

    @staticmethod
    def decrypt(msg: bytes, pri_key, max_length=128):
        """
        先将编码后的消息用base64解码，然后用私钥解密
        :param msg: 被 base64 编码后的消息密文
        :type: bytes
        :param pri_key: 私钥
        :param max_length: 最大一次解密长度(超过则进行分段解密)
        :return: 消息明文
        :rtype: str
        """
        msg = base64.b64decode(msg)
        if len(msg) <= max_length:
            return rsa.decrypt(msg, pri_key).decode()
        else:
            tmp_result = ''
            while msg:
                tmp_msg = msg[:max_length]
                msg = msg[max_length:]
                tmp_result += rsa.decrypt(tmp_msg, pri_key).decode()
            return tmp_result


class Database:
    """
    数据库，用来存取信息
    数据库中保存了用户名、密码以及各账户的公私钥
    """
    def __init__(self, database_name='database.sqlite'):
        self.database = sqlite3.connect(database_name, check_same_thread=False)

    @staticmethod
    def md5_encode(password: str):
        """
        将输入字符串进行 MD5 加密，基本用于数据库中密码加密
        :param password: 输入的密码字符串
        :return: MD5 加密后的密码
        """
        md5_encoder = hashlib.md5()
        md5_encoder.update((PREFIX_SALT+password+SUFFIX_SALT).encode())
        return md5_encoder.hexdigest()

    # 生成的 rsa 密钥的文件名
    def generate_key(self, length=64, low_az=True, up_az=True, n09=True, special_symbol=False):
        """
        生成随机的密钥，可以自定义组成元素和长度
        :param length: 密钥长度
        :param low_az: 是否使用小写字母
        :param up_az: 是否使用大写字母
        :param n09: 是否使用数字
        :param special_symbol: 是否使用特殊符号
        :return: 返回按规则生成的密钥
        """
        low_az_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        up_az_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        n09_alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        special_symbol_alphabet = ['!', '@', '.', '&', '_']
        result_key = ''
        alphabet = []
        if low_az:
            alphabet.extend(low_az_alphabet)
        if up_az:
            alphabet.extend(up_az_alphabet)
        if n09:
            alphabet.extend(n09_alphabet)
        if special_symbol:
            alphabet.extend(special_symbol_alphabet)
        while True:
            for each in range(length):
                result_key += alphabet[random.randint(0, len(alphabet) - 1)]
            if not self.filename_key_exist(result_key):
                break
        return result_key

    def init_database(self):
        """
        新建一个数据库 包含
        唯一序列号 创建时间 用户名 密码 RSA_public_key RSA_private_key 登陆状态 最后一次登录时间
        :return: None
        """
        # 创建 user 表
        sql = "CREATE TABLE IF NOT EXISTS user(" \
              "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
              "create_time date," \
              "username CHAR(20) UNIQUE," \
              "password CHAR(20)," \
              "RSA_public_key_location TEXT," \
              "RSA_private_key_location TEXT," \
              "login REAL," \
              "last_login_time date" \
              ")"
        self._database_operation(sql)
        # 创建密钥存储表
        sql = "CREATE TABLE IF NOT EXISTS rsa_key_filename(" \
              "filename CHAR(64) PRIMARY KEY)"
        self._database_operation(sql)

    def create_user(self, username: str, password: str):
        """
        根据 username 和 password 在 user 表中新建一个用户
        :param username: 用户名
        :param password: 用 md5 加密后的密码
        :return: None
        """
        rsa_public_key, rsa_private_key = rsa.newkeys(1024)
        rsa_public_key_location = self.generate_key()+'.pem'
        rsa_private_key_location = self.generate_key()+'.pem'
        with open(RSA_DEPOSITORY_LOCATION + rsa_public_key_location, 'wb') as f:
            f.write(rsa_public_key.save_pkcs1())
        with open(RSA_DEPOSITORY_LOCATION + rsa_private_key_location, 'wb') as f:
            f.write(rsa_private_key.save_pkcs1())
        rsa_public_key.save_pkcs1()
        create_time = time.strftime("%F %X")
        sql = f"INSERT INTO user VALUES(" \
              f"NULL,'{create_time}','{username}','{Database.md5_encode(password)}','{rsa_public_key_location}','{rsa_private_key_location}','true','{create_time}'" \
              f")"
        self._database_operation(sql)

    def del_user(self, username):
        """
        根据 username 删除一个用户
        :param username: 用户名
        :return: None
        """
        sql = f"SELECT RSA_public_key_location,RSA_private_key_location FROM user WHERE username='{username}'"
        rsa_public_key_location, rsa_private_key_location = self._database_select(sql)
        os.remove(RSA_DEPOSITORY_LOCATION + rsa_public_key_location)
        os.remove(RSA_DEPOSITORY_LOCATION + rsa_private_key_location)
        logging.info(f"Have been delete the rsa key of ({username})")
        sql = f"DELETE FROM user WHERE username='{username}'"
        self._database_operation(sql)
        logging.info(f"have been remove the item of ({username})")
        logging.info(f"remove successfully")

    def get_user_rsa_key(self, username: str):
        """
        根据 username 从数据库中查找到相应的 rsa_public_key 和 rsa_private_key，用来识别客户端的数据
        :param username: 要查找的 username
        :return: 一个包含 rsa_public_key 和 rsa_private_key 的元组
        """
        sql = f"SELECT RSA_public_key_location,RSA_private_key_location FROM user WHERE username='{username}'"
        result = self._database_select(sql)
        if not result:
            return NOT_FOUND
        else:
            rsa_public_key_location, rsa_private_key_location = result[0]
            with open(RSA_DEPOSITORY_LOCATION + rsa_public_key_location, 'rb') as f:
                rsa_public_key = rsa.PublicKey.load_pkcs1(f.read())
            with open(RSA_DEPOSITORY_LOCATION + rsa_private_key_location, 'rb') as f:
                rsa_private_key = rsa.PrivateKey.load_pkcs1(f.read())
            return rsa_public_key, rsa_private_key

    def get_user_password(self, username: str):
        """
        根据 username 从数据库中查找相应的 password 以识别登录请求是否合法
        :param username: 要查找的 username
        :return: MD5加密后的 password
        """
        sql = f"SELECT password FROM user WHERE username='{username}'"
        result = self._database_select(sql)
        if not result:
            return NOT_FOUND
        else:
            return result[0][0]

    def update_login_time(self, username: str):
        """
        更新用户最后登录时间
        :param username: 要更新的用户名
        :return: None
        """
        login_time = time.strftime("%F %X")
        sql = f"UPDATE user SET last_login_time='{login_time}' WHERE username='{username}'"
        self._database_operation(sql)

    def filename_key_exist(self, file_name: str):
        sql = f"SELECT * FROM rsa_key_filename WHERE filename='{file_name}'"
        result = self._database_select(sql)
        if result:
            return True
        else:
            return False

    def _database_operation(self, sql: str):
        """
        对数据库进行操作，无返回值
        :param sql: 要执行的 sql 语句
        :return: None
        """
        cur = self.database.cursor()
        cur.execute(sql)
        self.database.commit()
        cur.close()

    def _database_select(self, sql: str):
        """
        对数据库的查询，返回所有找到的结果
        :param sql: 要执行的 sql 语句
        :return: 查询到的 list，如果是查询多项数据，则每一个条目都返回一个元组
        """
        cur = self.database.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        return result


class Deck:
    def __init__(self):
        self.cards = []

    def get_card(self):
        """
        从卡组中抽一张牌
        :return:
        """
        return self.cards.pop()

    def shuffle(self, fold: list):
        """
        用弃牌堆中的牌洗牌
        :param fold: 弃牌堆卡组
        :return:
        """
        # 只有牌堆为空的时候才需要洗牌
        self.cards = []
        # 随机取弃牌堆中一张牌插入到牌堆中，直到弃牌堆为空
        while fold:
            # randint左右都能取到
            index = random.randint(0, len(fold)-1)
            self.cards.append(fold.pop(index))

    def __str__(self):
        print('当前卡组中的牌为: ')
        pprint(self.cards)
        return '——END——'

