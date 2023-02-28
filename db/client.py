from pymongo import MongoClient

#------------ Local database-----------------#
# Ejecutar db en local:
# MacOs: mongod --dbpath "/Users/diegosanchez/didacdev/Workspace/MongoDB/data"
# Windows: ./mongod --dbpath C:\Users\Diego\didacdev\Workspace\Mongodb\data
db_client = MongoClient().local

#------------Remote database-----------------#
# url = ""
# db_client = MongoClient(url, tlsAllowInvalidCertificates=True).test