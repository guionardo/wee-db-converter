import unittest

from src.config import Config


class TestConfig(unittest.TestCase):

    def test_config_failed(self):
        with self.assertRaises(ValueError):
            Config(dict(NOT_USED='1234'))

    def test_config(self):
        config = Config(dict(MYSQL_HOST='conn1',
                             MYSQL_PORT='3389',
                             MYSQL_DATABASE='db',
                             MYSQL_USER='user',

                             MYSQL_PASS='1234',
                             MONGO_CONNECTION_STRING='conn2'))
        self.assertEqual('conn1', config.MYSQL_HOST)
        self.assertEqual('conn2', config.MONGO_CONNECTION_STRING)
