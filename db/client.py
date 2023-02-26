from pymongo import MongoClient

#------------ Base de datos local-----------------#
# Ejecutar db en local: mongod --dbpath "/Users/diegosanchezescribano/didacdev/Workspace/MongoDB/data"
db_client = MongoClient().local

#------------Base de datos remota-----------------#
# url = "mongodb+srv://test:test@cluster0.sgeiq4z.mongodb.net/?retryWrites=true&w=majority"
# db_client = MongoClient(url, tlsAllowInvalidCertificates=True).test