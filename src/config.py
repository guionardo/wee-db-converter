import os


class Config:

    __slots__ = ['MYSQL_HOST',
                 'MYSQL_USER',
                 'MYSQL_PASS',
                 'MYSQL_DATABASE',
                 'MYSQL_PORT',
                 'MONGO_CONNECTION_STRING',
                 'MONGO_DATABASE',
                 'MONGO_COLLECTION']

    def __init__(self, source: dict = os.environ):
        self.MYSQL_HOST: str = ''
        self.MYSQL_USER: str = ''
        self.MYSQL_PASS: str = ''
        self.MYSQL_DATABASE: str = ''
        self.MYSQL_PORT: str = ''
        self.MONGO_CONNECTION_STRING: str = ''
        self.MONGO_DATABASE: str = ''
        self.MONGO_COLLECTION: str = ''
        self._load_source(source)

    def _load_source(self, source: dict):
        for env in self.__slots__:
            value = source.get(env)
            if not value:
                raise ValueError('Expected environment', env)

            setattr(self, env, value)
