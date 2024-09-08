from pymongo import MongoClient
connection_string = 'mongodb+srv://minanatansh:DYDoAsfdzqta5ay9@natansh2004.y0fuz.mongodb.net/?retryWrites=true&w=majority&appName=Natansh2004'
client = MongoClient(connection_string)  # connection
database = client['Farmer']
collection = database['FarmerData']

documents = collection.find()
# find() function == select * from table;

for i in documents:
    print(i)

print('Thank You!!')

# execute this file to fetch your data from database using python program