import pymongo
from pydantic import BaseModel
from pymongo.errors import PyMongoError


class MongoManager:
    bd = None

    @classmethod
    def id_to_string(cls, document):
        try:
            document["_id"] = str(document["_id"])
        except(KeyError, TypeError):
            pass
        return document

    @classmethod
    def to_list(cls, cursor):
        res = []
        for el in cursor:
            res.append(cls.id_to_string(el))
        return res

    @classmethod
    def check_if_exist(cls, query):
        res = cls.db.count_documents(query)
        if not res:
            return False
        return True
    #
    # @classmethod
    # def get_document(cls, query, **kwargs):
    #     document = cls.db.find_one(query, **kwargs)
    #     return cls.id_to_string(document)
    #
    # @classmethod
    # def get_documents(cls, query, **kwargs):
    #     document = cls.db.find(query, **kwargs)
    #     return cls.to_list(document)
    #
    # @classmethod
    # def create_document(cls, data, key):
    #     model: BaseModel = cls.types[key]
    #     validated_model = model.model_validate(data)
    #     return cls.db.insert_one(validated_model.model_dump())

    @classmethod
    def update_document(cls,query,update,**kwargs):
        document = cls.db.find_one_and_update(query,update,return_document=pymongo.ReturnDocument.AFTER,**kwargs)
        return cls.id_to_string(document)

    # @classmethod
    # def delete_document(cls,query,**kwargs):
    #     document = cls.db.find_one_and_delete(query,**kwargs)
    #     return document
    #
    # @classmethod
    # def delete_documents(cls,query,**kwargs):
    #     try:
    #         result = cls.db.delete_many(query,**kwargs)
    #         return result.deleted_count
    #     except PyMongoError:
    #         return None

