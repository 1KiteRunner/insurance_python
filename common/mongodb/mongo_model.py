import cPickle
import time
from urllib import quote_plus
import pymongo
from bson import ObjectId
from common.config import mongo_password, mongo_uri, mongo_user


class MongoModel(object):
    # mongo_url = 'mongodb://52.80.31.10:27017/'
    mongo_url = "mongodb://%s:%s@%s" % (quote_plus(mongo_user), quote_plus(mongo_password), mongo_uri)
    mongo = pymongo.MongoClient(mongo_url).Insurance

    @classmethod
    def get_one_data(cls, collection, _id):
        data = cls.mongo[collection].find_one({'_id': _id})
        return data if data else None

    def set(self, collection, obj):
        return self.mongo[collection].update({'_id': getattr(obj, '_id')}, obj.value_data)

    def update(self, collection, obj):
        return self.mongo[collection].update({'_id': ObjectId(getattr(obj, '_id'))}, obj.value_data)

    def update_one(self, collection, query, data):
        return self.mongo[collection].update(query, data)

    def update_insert(self, collection, query, data, upsert=True):
        return self.mongo[collection].update(query, data, upsert=upsert)

    def insert(self, collection, data):
        return self.mongo[collection].insert(data)

    @classmethod
    def find(cls, collection, query, **kwargs):
        if not kwargs:
            kwargs = None
        data = cls.mongo[collection].find_one(query, kwargs)
        return data if data else None

    @classmethod
    def find_data(cls, collection, query, **kwargs):
        if not kwargs:
            kwargs = None
        data_list = cls.mongo[collection].find(query, kwargs)
        return [data for data in data_list] if data_list else None

    @classmethod
    def remove_data(cls, collection, query):

        return cls.mongo[collection].remove(query)

    @classmethod
    def find_data_page(cls, collection, query, page, nbr, **kwargs):
        if not kwargs:
            kwargs = None
        data_list = cls.mongo[collection].find(query, kwargs).skip((page - 1) * nbr).limit(nbr)
        return [data for data in data_list] if data_list else None

    @classmethod
    def find_one_and_delete(cls, collection, _id):
        return cls.mongo[collection].find_one_and_delete({'_id': _id})

    @classmethod
    def count(cls, collection, query, **kwargs):
        if not kwargs:
            kwargs = None
        return cls.mongo[collection].find(query, kwargs).count()

    @classmethod
    def find_origin_data(cls, collection, query, **kwargs):
        if not kwargs:
            kwargs = None
        origin_data = cls.mongo[collection].find(query, kwargs)
        return origin_data

    @classmethod
    def aggregate(cls, collection, statement):
        output = cls.mongo[collection].aggregate(statement)
        # if output['ok'] == 1.0:
        #     return output['result']
        # else:
        #     return None
        return list(output)


class BaseModel(MongoModel):
    collection = None
    fields = None

    object_key = '{name}:obj:{_id}'

    @classmethod
    def init(cls):
        return cls.load({"create_at": time.time()})

    @classmethod
    def get_one(cls, _id):
        data = super(BaseModel, cls).get_one_data(cls.collection, ObjectId(_id))
        return cls.load(data) if data else None

    @classmethod
    def get_list(cls, _ids):
        return [cls.get_one(ObjectId(_id)) for _id in _ids if
                cls.get_one(ObjectId(_id))] if _ids else []

    @classmethod
    def get(cls, _id):
        data = super(BaseModel, cls).get_one_data(cls.collection, ObjectId(_id))
        return cls.load(data) if data else None

    @classmethod
    def find_one_data(cls, query, **kwargs):
        data = cls.find(cls.collection, query, **kwargs)
        return cls.load(data) if data else None

    @classmethod
    def get_count(cls, query=None, **kwargs):
        return cls.count(cls.collection, query, **kwargs)

    def put(self):
        return self.set(self.collection, self)

    @classmethod
    def find_data_list(cls, query=None, **kwargs):
        return cls.find_data(cls.collection, query, **kwargs)

    @classmethod
    def delete_data(cls, query=None):
        return cls.remove_data(cls.collection, query)

    @classmethod
    def find_data_obj(cls, query=None, **kwargs):
        data_list = cls.find_data(cls.collection, query, **kwargs)
        return [cls.load(data) for data in data_list] if data_list else None

    @classmethod
    def find_data_paging(cls, query=None, page=1, nbr=20, **kwargs):
        return cls.find_data_page(cls.collection, query, page, nbr, **kwargs)

    def create_model(self, **kwargs):
        [setattr(self, attr, value) for attr, value in kwargs.items()]
        data = self.value_data
        if '_id' in data.keys():
            data.pop("_id")
        ret = self.insert(self.collection, data)
        return ret

    def edit_model(self, **kwargs):
        [setattr(self, attr, value) for attr, value in kwargs.items() if attr != '_id']
        self.update(self.collection, self)

        return

    @classmethod
    def delete_model(cls, _id):
        ret = cls.find_one_and_delete(cls.collection, _id)

        return ret

    @property
    def value_data(self):
        obj_dict = self.__dict__
        return {field: obj_dict.get(field, '') for field in self.fields}

    @classmethod
    def load(cls, data):
        obj = cls()
        [setattr(obj, k, data.get(k)) for k in data if data]
        return obj

    def format(self):
        obj_dict = self.__dict__
        data = dict()
        for field in self.fields:
            if isinstance(obj_dict.get(field, ''), ObjectId):
                data[field] = str(obj_dict.get(field, ''))
            else:
                data[field] = obj_dict.get(field, '')

        return data

    @classmethod
    def aggregate_data(cls, statement):
        return super(BaseModel, cls).aggregate(cls.collection, statement)


if __name__ == "__main__":
    client = MongoModel()
    client.insert('InsuranceInfo', {'aaa': 'asd'})
