from BitHash import BitHash, ResetBitHash

class CuckooHash(object):
    
    def __init__(self, size):
        
        #initialize 2 hashtables - lists of (key, [data])
        self.__table1 = [None] * size
        self.__table2 = [None] * size
        
        self.__numBuckets = size
        
        #set a threshold number of times to loop when inserting
        self.__maxLoop = 16
        
        #keep track of the number of keys inserted into the hashtables
        #to ensure that they don't get too full
        self.__numKeys = 0
    
    
    #return the first potential nest for a key - an index in table 1  
    def __h1(self, key):
        return BitHash(key) % self.__numBuckets
    
    #return the second potential spot to insert a key - an index in table 2.
    #rehash using the first hash value as the seed.
    def __h2(self, key):
        return BitHash(key, BitHash(key)) % self.__numBuckets
    
    
    #search for a key in the cuckoo hash.
    #if the key is found, return which hashtable it was found in and its data. 
    def find(self, key):
        
        #if the key is stored in the first hashtable
        #(this line avoids indexing into a nonexistent tuple)
        if self.__table1[self.__h1(key)] and \
           self.__table1[self.__h1(key)][0] == key:
                
                #return which table the key was found in
                #and the key's associated data
                return (1, self.__table1[self.__h1(key)][1])
            
        #if the key is stored in the second hashtable
        elif self.__table2[self.__h2(key)] and \
            self.__table2[self.__h2(key)][0] == key:
                
                #return which table the key was found in
                #and the key's associated data
                return (2, self.__table2[self.__h2(key)][1])
        
        #if the key is not found, return None
        return None
     
     
    #insert a key-data pair into the cuckoo hash.
    #if the key is already in the cuckoo hash, append the new data
    #to the current data.
    def insert(self, key, data):
        a = self.__insert(key, data)
        return a

    #insert a key-data pair into the cuckoo hash - private method
    #called by the public insert method
    def __insert(self, key, data):
        #if the key is already in the cuckoo hash,
        #append the data to the key's existing data
        if self.find(key):
            if self.find(key)[0] == 1:
                # self.__table1[self.__h1(key)][1].append(data)
                return (self.__table1[self.__h1(key)][1], (data))
            elif self.find(key)[0] == 2:
                # self.__table2[self.__h2(key)][1].append(data)
                return (self.__table2[self.__h2(key)][1], (data))
            # return
        
        #if the cuckoo hash is getting too full, double its size
        if self.__numKeys >= .5 * self.__numBuckets:
            self.__growTables()
            
        #if the key is not in the cuckoo hash
        #create a tuple with the key and data to insert
        keyData = (key, data)
        
        #up to maxloop times:
        for i in range(self.__maxLoop):
            
            #if the first possible nest for the key is empty,
            #insert it there and increment numKeys
            if not self.__table1[self.__h1(keyData[0])]:
                self.__table1[self.__h1(keyData[0])] = keyData
                self.__numKeys += 1
                # print(keyData)
                return
            
            #otherwise, evict the current occupant of the nest
            #and insert the key in the nest
            temp = self.__table1[self.__h1(keyData[0])]
            self.__table1[self.__h1(keyData[0])] = keyData
            keyData = temp
            
            #try to insert the evicted key in the second table
            if not self.__table2[self.__h2(keyData[0])]:
                self.__table2[self.__h2(keyData[0])] = keyData
                self.__numKeys += 1
                # print(keyData)
                return
            
            #if that nest is full, evict its occupant
            temp = self.__table2[self.__h2(keyData[0])]
            self.__table2[self.__h2(keyData[0])] = keyData
            keyData = temp
            
            #keep looping and inserting evicted keys until a key is inserted
            #into an empty nest. if maxLoop is reached before that happens,
            #assume we have entered an infinite loop.
        
        #if we have encountered an infinite loop, rehash all keys
        #in the cuckoo hash and then try to insert the current key again.
        self.__rehash()
        
        #if insertion fails after rehashing, double the size of the hash tables
        #and then try to insert the key again.
        if not self.__insert(keyData[0], keyData[1]):
            
            self.__growTables()
            self.__insert(keyData[0], keyData[1])    
    
    
    #rehash all keys in the cuckoo hash with new hash functions        
    def __rehash(self):


        #reset the hash functions so that future calls to h1 and h2
        #will return different hash values from different hash functions
        ResetBitHash()
        
        #create 2 new hash tables
        newTab1 = [None] * (self.__numBuckets)
        newTab2 = [None] * (self.__numBuckets)
        
        #re-insert the key-data pairs from the old hash tables into the
        #new ones using the updated hash functions
        for keyData in self.__table1:
            if keyData:
                for i in range(self.__maxLoop):
                    if not newTab1[self.__h1(keyData[0])]:
                        newTab1[self.__h1(keyData[0])] = keyData
                        break
                    temp = newTab1[self.__h1(keyData[0])]
                    newTab1[self.__h1(keyData[0])] = keyData
                    keyData = temp  
                    if not newTab2[self.__h2(keyData[0])]:
                        newTab2[self.__h2(keyData[0])] = keyData
                        break   
                    temp = newTab2[self.__h2(keyData[0])]
                    newTab2[self.__h2(keyData[0])] = keyData
                    keyData = temp
        
        for keyData in self.__table2:
            if keyData:
                for i in range(self.__maxLoop):
                    if not newTab1[self.__h1(keyData[0])]:
                        newTab1[self.__h1(keyData[0])] = keyData
                        break
                    temp = newTab1[self.__h1(keyData[0])]
                    newTab1[self.__h1(keyData[0])] = keyData
                    keyData = temp  
                    if not newTab2[self.__h2(keyData[0])]:
                        newTab2[self.__h2(keyData[0])] = keyData
                        break
                    temp = newTab2[self.__h2(keyData[0])]
                    newTab2[self.__h2(keyData[0])] = keyData
                    keyData = temp            
        
        #replace the old hashtables with the new ones        
        self.__table1 = newTab1
        self.__table2 = newTab2    
       
        
    #double the size of the 2 hash tables and reinsert all keys        
    def __growTables(self):

        # print(True)
        
        #create 2 new hashtables twice as long as the old ones
        self.__numBuckets *= 2
        newTab1 = [None] * (self.__numBuckets)
        newTab2 = [None] * (self.__numBuckets)
        
        #re-insert the key-data pairs from the old hash tables into the
        #new ones with hash values spanning the range of the new tables
        for keyData in self.__table1:
            if keyData:
                for i in range(self.__maxLoop):
                    if not newTab1[self.__h1(keyData[0])]:
                        newTab1[self.__h1(keyData[0])] = keyData
                        break
                    temp = newTab1[self.__h1(keyData[0])]
                    newTab1[self.__h1(keyData[0])] = keyData
                    keyData = temp  
                    if not newTab2[self.__h2(keyData[0])]:
                        newTab2[self.__h2(keyData[0])] = keyData
                        break   
                    temp = newTab2[self.__h2(keyData[0])]
                    newTab2[self.__h2(keyData[0])] = keyData
                    keyData = temp
        
        for keyData in self.__table2:
            if keyData:
                for i in range(self.__maxLoop):
                    if not newTab1[self.__h1(keyData[0])]:
                        newTab1[self.__h1(keyData[0])] = keyData
                        break
                    temp = newTab1[self.__h1(keyData[0])]
                    newTab1[self.__h1(keyData[0])] = keyData
                    keyData = temp  
                    if not newTab2[self.__h2(keyData[0])]:
                        newTab2[self.__h2(keyData[0])] = keyData
                        break
                    temp = newTab2[self.__h2(keyData[0])]
                    newTab2[self.__h2(keyData[0])] = keyData
                    keyData = temp            
        
        #replace the old hashtables with the new ones         
        self.__table1 = newTab1
        self.__table2 = newTab2
        
     
    #remove a key and its associated data from the cuckoo hash
    def delete(self, key):

        #if the key is found, set its nest to None
        if self.find(key):
            if self.find(key)[0] == 1:
                self.__table1[self.__h1(key)] = None
            else:
                self.__table2[self.__h2(key)] = None
            
            #decrement the number of keys in the cuckoo hash
            self.__numKeys -= 1
    
    
    #return the number of keys stored in the cuckoo hash            
    def numKeys(self):
        return self.__numKeys

    def Keys(self):
        return self.__table1, self.__table2
