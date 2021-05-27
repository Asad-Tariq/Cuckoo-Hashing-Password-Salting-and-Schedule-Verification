from CuckooHash import CuckooHash
import random

def words():
    word = ["hey", "hell", "something", "life", "red", "blue", "green", "pale", "jail", "habib"]
    num = random.randint(0, 9)
    return word[num]

CH = CuckooHash(10)
counter = 0
for i in range(100):
    word = words()
    a = CH.insert(word, random.randint(1, 10))
    if a is not None:
        print(a[0][0], a[1][0])
        print(a[0][1], a[1][1])
    # else:
    #     print(a, "Hello")
# a, b, c = CH.numKeys()
# print(b)
# print(c)

counter += CH.numKeys()
if counter == 10:
    print("successful")


# import random, time

# def randWord():
#     random.seed(time.time())
#     string = ""
#     for _ in range(32):
#         letter = chr(random.randint(33, 126))
#         string += letter
#     return string

# password = "something"
# salt = randWord()

# alteredpassword = salt[:int(len(salt)/2)] + password + salt[int(len(salt)/2):]
# print(len(salt[:int(len(salt)/2)]))
# print(len(salt[int(len(salt)/2):]))
# print(len(alteredpassword))
# print(alteredpassword)