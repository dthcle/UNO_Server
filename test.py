from util import *
from util import response_encoder
from PROTOCOL import LOGIN_PROTOCOL
# from util import database

# database.init_database()

database.create_user('dthcle', 'admin_dthcle')

# print(response_encoder(LOGIN_PROTOCOL, {"username": "username_test"}))

# rsa_public_key, rsa_private_key = database.get_user_rsa_key('username_test')
# test_str = database.generate_key(length=118)
# print(test_str)
# code = RSACrypto.encrypt(test_str, rsa_public_key)
# print(code)
# result = RSACrypto.decrypt(code, rsa_private_key)
# print(result)

