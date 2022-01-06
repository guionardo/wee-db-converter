import json
import urllib.parse
import os
from typing import Tuple, Union

import pymongo
from src.config import Config
from src.repositories.base_output_repository import BaseOutputRepository


class MongoDbOutputRepository(BaseOutputRepository):

    def __init__(self, config: Config) -> None:
        self._config: Config = config
        cs = urllib.parse.quote_plus(self._config.MONGO_CONNECTION_STRING)
        self._client = pymongo.MongoClient(cs)
        self._database = self._client.get_database(self._config.MONGO_DATABASE)
        self._collection = self._database.get_collection(
            self._config.MONGO_COLLECTION)

    def save(self, id: int, data: dict) -> Union[Exception, None]:
        data['_id'] = data['post_id']
        try:
            result = self._collection.replace_one({'_id': data['post_id']},
                                                  data, upsert=True)
            print(result)
        except Exception as exc:
            return exc

    def get(self, id: int) -> Tuple[dict, Exception]:
        raise NotImplementedError

    def delete(self, id: int) -> Union[Exception, None]:
        raise NotImplementedError
