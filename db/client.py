from pymongo import MongoClient

#------------ Local database-----------------#
# Ejecutar db en local: mongod --dbpath [path to your data directory]
db_client = MongoClient().local

#------------Remote database-----------------#
# url = [url to your remote database]
# uncomment the following line
# db_client = MongoClient(url, tlsAllowInvalidCertificates=True).test