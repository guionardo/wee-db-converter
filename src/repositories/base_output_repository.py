from typing import Protocol, Tuple, Union


class BaseOutputRepository(Protocol):

    def save(self, id: int, data: dict) -> Union[Exception, None]:
        raise NotImplementedError

    def get(self, id: int) -> Tuple[dict, Exception]:
        raise NotImplementedError

    def delete(self, id: int) -> Union[Exception, None]:
        raise NotImplementedError
