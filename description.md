# 服务器与客户端工作流程
## 数据传输结构
客户端请求结构
```json
{
  "request": request_protocol,
  "data": {
    "data_name": data_content
  }
}
```
服务器返回结构
```json
{
  "response": response_code,
  "data": {
    "data_name": data_content  
  }
}
```
## 流程
1. 打开客户端，输入用户名和密码，登录进入游戏
```json
{
  "request": LOGIN_PROTOCOL,
  "data": {
    "username": username,
    "password": password
  }
}
```
2. 服务器接收到登录请求后，判断是否合法，合法就进入游戏，并返回客户端的地址
登陆成功
```json
{
  "response": STATUS_ALL[OK],
  "data": {
    "client_addr": client_addr
  }
}
```
登陆失败
```json
{
  "response": STATUS_ALL[USERNAME_PASSWORD_WRONG],
  "data": {}
}
```
3. 客户端输入期望游戏人数，点击匹配

此时打开了一个对服务器的tcp连接，向服务器发送了一个数据包，并创建了一个接受服务器数据发送的服务端(客户端用来接收游戏数据)
```json
{
  "request": MATCH_PROTOCOL,
  "data": {
    "client_port": client_port,
    "player_num": player_num
  }
}
```
4. 服务器接受客户端的连接请求，并接受数据包

将客户端的ip加入到等待队列，如果匹配人数足够就开启游戏服务器，并在游戏服务器上发送对客户端的连接请求
```json
{
  "response": GAME_INIT_PROTOCOL,
  "data": {}
}
```
此时客户端返回一个数据包，告诉游戏服务器自己是谁(待优化)
```json
{
  "request": CHECK_USER_IDENTITY_PROTOCOL,
  "data": {
    "username": username
  }
}
```
5. 服务器分清楚各玩家后，开始使用RSA加密进行数据传输(直接明文传输rsa的公钥)
```json
{
  "response": GAME_START_PROTOCOL,
  "data": {
    // true 是顺时针 false 是逆时针
    "direction": true,
    // 获取各玩家的手牌数，玩家顺序为逆时针
    "players_list": [player_username_1, player_username_2, player_username_3, player_username_4],
    "hand_card_num_list": [num_of_hand_1, num_of_hand_2, num_of_hand_3, num_of_hand_4],
    "hand_card": [code_of_card, code_of_card],
    // 轮到哪个玩家出牌
    "allow_to_discard": player_username,
    // 引导牌
    "the_guide": code_of_card,
    // RSA公私钥
    "rsa_public_key": rsa_public_key,
    "rsa_private_key": rsa_private_key
  }
}
```
6. (循环)玩家收到服务器的信号后

PS: 从此处开始加密

出牌的玩家(username == username)
```json
{
  "request": USER_DISCARD_PROTOCOL,
  "data": {
    "card_code": card_code,
    "guide_color": guide_color
  }
}
```
服务器接受信号后

判断是否符合出牌规则 否则让该玩家重新出牌(将已出的牌收回)
 ```json
{
  "request": STATUS_ALL[IRREGULAR_DATA],
  "data": {
    "error_card_code": card_code
  }
}
```
 
 根据服务器上的数据判断下一个出牌玩家是谁
 ```json
{
  "response": GAME_RUN_PROTOCOL, 
  "data": {
    // true 是逆时针 false 是顺时针
    "direction": true,
    // 获取各玩家的手牌数，玩家顺序为逆时针
    "player_hand_num_list": {
      player_username_1: num_of_hand_1,
      player_username_2: num_of_hand_2,
      player_username_3: num_of_hand_3,
      player_username_4: num_of_hand_4
    },
    "hand_card": [code_of_card, code_of_card],
    // 轮到哪个玩家出牌
    "allow_to_discard": player_username,
    // 引导牌
    "the_guide": code_of_card,
  }
}
```


