import os 
import hashlib
import json

users = {}

username = input('Enter your username: ')
password = input('Enter your password: ')

# user_salt = os.urandom(32)
pass_salt = os.urandom(32)

#128 byte key if not provided, will default to SHA-256 size of 64 bytes
# user_hash = hashlib.pbkdf2_hmac('sha256', username.encode('utf-8'), b'salt', 100000, dklen = 128)
pass_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), pass_salt, 100000, dklen = 128)

users[username] = {'Pass Hash': pass_hash.decode('latin-1'), 'Pass Salt': pass_salt.decode('latin-1')}

with open('users.txt', 'w') as outfile:
    json.dump(users, outfile)
