class CARD_COLOR:
    RED = 'R'
    BLUE = 'B'
    YELLOW = 'Y'
    GREEN = 'G'
    UNIVERSAL = 'U'


class CARD_CONTENT:
    N_0 = '0'
    N_1 = '1'
    N_2 = '2'
    N_3 = '3'
    N_4 = '4'
    N_5 = '5'
    N_6 = '6'
    N_7 = '7'
    N_8 = '8'
    N_9 = '9'
    BLOCK = '10'
    REVERSE = '11'
    ADD2 = '12'
    CHANGE = '13'
    ADD4 = '14'


class CARD_CODE:
    # 获取卡牌的编号(颜色, 内容)
    @staticmethod
    def get_card_code(color, content):
        return color, content


# from util import return_the_full_deck
# # 用来初始化牌堆的完整牌堆
# FULL_DECK = return_the_full_deck()
FULL_DECK = [('R', '0'), ('R', '1'), ('R', '2'), ('R', '3'), ('R', '4'), ('R', '5'), ('R', '6'), ('R', '7'), ('R', '8'),
             ('R', '9'), ('R', '10'), ('R', '11'), ('R', '12'), ('R', '1'), ('R', '2'), ('R', '3'), ('R', '4'),
             ('R', '5'), ('R', '6'), ('R', '7'), ('R', '8'), ('R', '9'), ('R', '10'), ('R', '11'), ('R', '12'),
             ('B', '0'), ('B', '1'), ('B', '2'), ('B', '3'), ('B', '4'), ('B', '5'), ('B', '6'), ('B', '7'), ('B', '8'),
             ('B', '9'), ('B', '10'), ('B', '11'), ('B', '12'), ('B', '1'), ('B', '2'), ('B', '3'), ('B', '4'),
             ('B', '5'), ('B', '6'), ('B', '7'), ('B', '8'), ('B', '9'), ('B', '10'), ('B', '11'), ('B', '12'),
             ('Y', '0'), ('Y', '1'), ('Y', '2'), ('Y', '3'), ('Y', '4'), ('Y', '5'), ('Y', '6'), ('Y', '7'), ('Y', '8'),
             ('Y', '9'), ('Y', '10'), ('Y', '11'), ('Y', '12'), ('Y', '1'), ('Y', '2'), ('Y', '3'), ('Y', '4'),
             ('Y', '5'), ('Y', '6'), ('Y', '7'), ('Y', '8'), ('Y', '9'), ('Y', '10'), ('Y', '11'), ('Y', '12'),
             ('G', '0'), ('G', '1'), ('G', '2'), ('G', '3'), ('G', '4'), ('G', '5'), ('G', '6'), ('G', '7'), ('G', '8'),
             ('G', '9'), ('G', '10'), ('G', '11'), ('G', '12'), ('G', '1'), ('G', '2'), ('G', '3'), ('G', '4'),
             ('G', '5'), ('G', '6'), ('G', '7'), ('G', '8'), ('G', '9'), ('G', '10'), ('G', '11'), ('G', '12'),
             ('U', '13'), ('U', '14'), ('U', '13'), ('U', '14'), ('U', '13'), ('U', '14'), ('U', '13'), ('U', '14')]

# QUANTITY
DATA_PACK_MAX_SIZE = 2048

# MD5 SALT
PREFIX_SALT = 'prefix_salt'
SUFFIX_SALT = 'suffix_salt'

# SERVER
MATCH_SERVER_ADDR = '127.0.0.1'
MATCH_SERVER_PORT = 20000

GAME_SERVER_ADDR = '127.0.0.1'
GAME_SERVER_PORT_MIN = 21000
GAME_SERVER_PORT_MAX = 22000

# Client
CLIENT_DEFAULT_PORT = 23000
CLIENT_PUBLIC_KEY_INDEX = 0
CLIENT_PRIVATE_KEY_INDEX = 1

CLIENT_ADDR_INDEX = 0
CLIENT_PORT_INDEX = 1

# DATABASE
NOT_FOUND = 'NOT_FOUND_INFO'

# ENCODE
RSA = 'rsa'

# RSA DEPOSITORY
RSA_DEPOSITORY_LOCATION = './rsa_depository/'

# HOW TO PLAY
BEGINNING_HAND_CARD_NUM = 7

# JSON KEY
J_USERNAME = 'username'
J_PASSWORD = 'password'
J_CLIENT_ADDR = 'client_addr'
J_CLIENT_PORT = 'client_port'
J_PLAYER_NUM = 'player_num'
J_DIRECTION = 'direction'
J_PLAYER_HAND_NUM_LIST = 'player_hand_num_list'
J_HAND_CARD = 'hand_card'
J_ALLOW_TO_DISCARD = 'allow_to_discard'
J_THE_FIRST_GUIDE = 'the_first_guide'
J_RSA_PUBLIC_KEY = 'rsa_public_key'
