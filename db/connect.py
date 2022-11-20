import pymongo
print("Welcome")
client=pymongo.MongoClient("mongodb+srv://dannymongo:nrkXZB2c1PEL0TfG@cluster0.oq7u4bt.mongodb.net/test")
# localhost 
# client=pymongo.MongoClient("mongodb://localhost:27017") 
print(client)
db=client['todo']
collections=db['todocollection']