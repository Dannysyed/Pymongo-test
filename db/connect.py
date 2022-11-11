import pymongo
print("Welcome")
client=pymongo.MongoClient("mongodb://localhost:27017")
print(client)
db=client['todo']
collections=db['todocollection']
print('Db was created')