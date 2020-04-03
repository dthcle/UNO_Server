from util import *
from util import response_encoder
from PROTOCOL import LOGIN_PROTOCOL
from util import database

# database.init_database()

# database.del_user('dthcle')
# database.create_user('dthcle', 'dthcle')

result = database.get_user_rsa_key("dthcle")
tmp = result[0].save_pkcs1(format='PEM').decode()
print(tmp)
print(rsa.PublicKey.load_pkcs1(tmp))
