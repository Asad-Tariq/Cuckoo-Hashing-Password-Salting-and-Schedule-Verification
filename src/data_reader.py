from CuckooHash import CuckooHash

from accounts_class import Accounts


def read_accounts():
    CH = CuckooHash(50) 
    f = open("C:/Users/fahad/Documents/Pycharm Projects/Project/Dummy Data/accounts.txt", "r")
    a = f.readlines()

    objs = []

    for i in a:
        a_string = i. rstrip("\n")
        acc_data = a_string.split(',')
        objs.append(Accounts(acc_data[0], acc_data[1], acc_data[2]))

    for j in objs:
        key, data = j.data()
        a = CH.insert(key, data)
    
    return CH

# a = read_accounts()
# b = a.find("Don_Winslow")
# print(b)