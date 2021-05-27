import pytest
from CuckooHash import CuckooHash
import random

#generate a random-length string of random letters, symbols, 
#and numbers to insert into the cuckoo hash
# def randWord():
#     num = random.randint(1, 10)
#     string = ""
#     for i in range(num):
#         letter = chr(random.randint(32, 126))
#         string += letter
#     return string

def words():
    word = ["hey", "hell", "something", "life", "red", "blue", "green", "pale", "jail", "habib"]
    num = random.randint(0, 9)
    return word[num]

#-------------TESTS---------------------

#assert that the number of words in the cuckoo hash equals the 
#number of words that were inserted into it
def test_insert():
    CH = CuckooHash(10000)
    counter = 0
    for i in range(1000):
        word = words()
        a = CH.insert(word, random.randint(1, 10))
    counter += CH.numKeys()
    assert counter == 10
        
#assert that all words inserted in the cuckoo hash are found in it
def test_find():
    CH = CuckooHash(10000)
    words_lst = []
    for i in range(1000):
        word = words()
        CH.insert(word, random.randint(1,100))
        words_lst.append(word)
    for word in words_lst:
        assert CH.find(word)

#test the delete method
def test_delete():
    CH = CuckooHash(10000)
    words_lst = []
    for i in range(1000):
        word = words()
        CH.insert(word, random.randint(1, 100))
        words_lst.append(word)
    for word in words_lst:
        CH.delete(word)

    #assert that there are zero keys in the cuckoo hash
    #after deleting every key that was inserted
    assert CH.numKeys() == 0

    #assert that attempts to find words in the cuckoo hash fail
    for i in range(100):
        assert not CH.find(words())


#insert many more keys than the size of the cuckoohash and
#assert that all keys are successfully inserted. this tests
#rehash and growTables.
def test_growHash():
    CH = CuckooHash(1)
    counter = 0
    for i in range(10000):
        word = words()
        CH.insert(word, random.randint(1,100))
    counter += CH.numKeys()
    assert counter == 10


#randomly insert and delete from the cuckoo hash and then ensure
#that the correct number of keys is stored in the cuckoo hash
def test_random():
    CH = CuckooHash(100)
    count = 0
    
    for i in range(10000):
        choice = random.randint(0,1)
        word = words()
        
        if choice == 0:
            if not CH.find(word):
                count += 1
            CH.insert(word, word)
            
        if choice == 1:
            if CH.find(word):
                count -= 1
            CH.delete(word)
            
    assert count == CH.numKeys()
        
    
pytest.main(["-v"])