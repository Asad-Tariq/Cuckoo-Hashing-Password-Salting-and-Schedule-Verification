from CuckooHash import CuckooHash

from accounts_class import Accounts

import random, time, hashlib

def generate_salt():
    random.seed(time.time())
    string = ""
    for _ in range(32):
        letter = chr(random.randint(33, 126))
        
        if letter == ',':
            letter = '-'

        string += letter
    return string

def generate_hash(salt, password):
    altered_password = salt[:int(len(salt)/2)] + password + salt[int(len(salt)/2):]
    hash_value = hashlib.sha256(altered_password.encode()).hexdigest()

    return hash_value

def update_data(username, salt, hash_value, password):
    f = open("C:/Users/fahad/Documents/Pycharm Projects/Project/Dummy Data/accounts.txt", "a")
    f.write('\n')
    f.write(username + ',' + salt + ',' + hash_value)
    f.close()

    f = open("C:/Users/fahad/Documents/Pycharm Projects/Project/Dummy Data/passwords.txt", "a")
    f.write('\n')
    f.write(password)
    f.close()

def user_account_add(username, password, cuckoo_hash):
    random_salt = generate_salt()
    hash_value = generate_hash(random_salt, password)
    cuckoo_hash.insert(username, (random_salt, hash_value))

    update_data(username, random_salt, hash_value, password)


