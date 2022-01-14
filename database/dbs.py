import logging
from typing import Any
from pymongo import MongoClient
from utils.config_reader import Config


class MongoConnectionFactory:
    __client = None

    @staticmethod
    def get_client(host: str, port: str, username: str, password: str, db: str):
        if MongoConnectionFactory.__client is None:
            con_str = f"mongodb://{username}:{password}@{host}:{port}/{db}?authSource=admin"
            MongoConnectionFactory.__client = MongoClient(con_str)
        return MongoConnectionFactory.__client


class MongoDB:
    def __init__(self):
        db_conf = Config.read_conf('db')
        self.__client = MongoConnectionFactory.get_client(db_conf.mongo.host, db_conf.mongo.port,
                                                          db_conf.mongo.username, db_conf.mongo.password,
                                                          db_conf.mongo.db)

        self.__db = self.__client[db_conf.mongo.db]
        self.__collection_mapping = db_conf.mongo.collection_mapping
        self.__logger = logging.Logger(__name__)

    def insert_document(self, collection_key: str, _id: Any = None, **kwargs):
        if len(kwargs) == 0:
            return

        if _id:
            kwargs.update({"_id": _id})

        collection = self.__db[self.__map_collection(collection_key)]
        doc = collection.insert_one(kwargs)
        return doc.inserted_id

    def insert_bulk_document(self, collection_key: str, docs: list):
        collection = self.__db[self.__map_collection(collection_key)]
        collection.insert_many(docs)

    def find_one(self, collection_key: str, **kwargs):
        if len(kwargs) == 0:
            return

        x = self.__db[self.__map_collection(collection_key)].find_one(kwargs)
        return x

    def __map_collection(self, collection_key: str):
        if collection_key in self.__collection_mapping.keys():
            return self.__collection_mapping[collection_key]
        else:
            return collection_key

    def close(self):
        self.__client.close()
