import json
import os
from typing import Tuple, Union

from src.config import Config
from src.repositories.base_output_repository import BaseOutputRepository


class FileOutputRepository(BaseOutputRepository):

    def __init__(self, config: Config):
        self._config: Config = config
        self._folder = os.path.join(os.path.abspath('.'), 'output')
        os.makedirs(self._folder, exist_ok=True)

    def _filename(self, id: int, suffix: str = '') -> str:
        return os.path.join(self._folder, f'{id:06d}{suffix}.json')

    def save(self, id: int, data: dict) -> Union[Exception, None]:
        try:
            with open(self._filename(id, data['post_type']), 'w') as file:
                json.dump(data, file, default=str)
        except Exception as exc:
            return exc

    def get(self, id: int) -> Tuple[dict, Exception]:
        try:
            with open(self._filename(id)) as file:
                return json.load(file)
        except Exception as exc:
            return exc

    def delete(self, id: int) -> Union[Exception, None]:
        try:
            fn = self._filename(id)
            if os.path.exists(fn):
                os.unlink(fn)
        except Exception as exc:
            return exc
