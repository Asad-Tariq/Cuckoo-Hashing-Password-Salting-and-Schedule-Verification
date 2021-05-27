class Accounts():

    def __init__(self, username, salt, hash_value):
        self.username = username
        self.salt = salt
        self.hash_value = hash_value

    def data(self):
        return self.username, (self.salt, self.hash_value)


# # password is saltedpassword

# username = "Jack_Sparrow"

# salt = "f1nd1ngn3m0"

# hash_value =  "d3fb99bf030efbfb8e12036b65d6954bc48715d038e55fa24cd62afa32764ae6"

# acc = Accounts(username, salt, hash_value)

# print(acc.data())

# f = open("accounts.txt", "r")
# a = f.readlines()

# objs = []

# for i in a:
#     a_string = i. rstrip("\n")
#     acc_data = a_string.split(',')
#     objs.append(Accounts(acc_data[0], acc_data[1], acc_data[2]))

# for j in objs:
#     print(j.data()) 


