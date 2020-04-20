import os 
import hashlib
import json


with open('users.txt') as json_file:
    data = json.load(json_file)

user_name = input('Enter a username: ')
if user_name in data:
    pass_key = data[user_name]['Pass Hash']
    pass_salt = data[user_name]['Pass Salt']
check_pass = input('Enter a password: ')

pass_hash = hashlib.pbkdf2_hmac('sha256', check_pass.encode('utf-8'), pass_salt.encode('latin-1'), 100000, dklen = 128)
print(pass_hash == pass_key.encode('latin-1'))
