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
    "accept_port": accept_port,
    "player_num": player_num
  }
}
```
4. 服务器接受客户端的连接请求，并接受数据包

将客户端的ip加入到等待队列，如果匹配人数足够就开启游戏服务器，并在游戏服务器上发送对客户端的连接请求
```json
{
  "response": GAME_START_PROTOCOL,
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
服务器分清楚各玩家后，开始使用RSA加密进行数据传输(直接明文传输rsa的公钥)
```json
{
  "response": GAME_START_PROTOCOL,
  "data": {
    // true 是逆时针 false 是顺时针
    "how_to_arrange_player": true,
    // 获取各玩家的手牌数，玩家顺序为逆时针
    "player_hand_num_list": [
      player_username_1 : num_of_hand_1,
      player_username_2 : num_of_hand_2,
      player_username_3 : num_of_hand_3,
      player_username_4 : num_of_hand_4
    ],
    "hand_card_increase_num": get_card_num,
    // 根据hand_card_increase_num获取应该获得手牌的数量，然后获取手牌对应的编号
    "hand_card": [
      "card_1": code_of_card,
      "card_2": code_of_card
    ],
    // 轮到哪个玩家出牌
    "player_to_discard": player_num,
    // 第一张引导牌
    "the_first_guide": code_of_card,
    // RSA公钥
    "rsa_public_key": rsa_public_key
  }
}
```

