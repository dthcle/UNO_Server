from util import *

# 初始化匹配服务端
match_server = MatchServer(MATCH_SERVER_ADDRESS, MATCH_SERVER_PORT)
# 初始化进程锁
lock = threading.Lock()
# 等待玩家的列表 字典对应的是玩家期望的游戏人数
# player_dict = {'4': []}
# test data
player_dict = {'1': []}
# 已开启服务器的端口的列表
server_port_list = []

while True:
    client_socket, client_addr = match_server.main_socket.accept()
    threading.Thread(target=match_server_get_client_request, args=(client_socket, client_addr, player_dict, server_port_list, lock)).start()




