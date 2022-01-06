import logging
from typing import Dict, List, Tuple, Union

import mysql.connector
from src.config import Config


def get_connector(config: Config) -> mysql.connector.connection:
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        database=config.MYSQL_DATABASE,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASS,
        port=int(config.MYSQL_PORT)
    )


class BaseRepository:

    def __init__(self, config: Config, table_name: str, id_field_name: str) -> None:
        self._config = config
        self._table_name = table_name
        self._id_field_name = id_field_name
        self._fields = []
        self.log = logging.getLogger(self.__class__.__name__)
        self.read_structure()

    def exec_sql(self, sql: str, args: Tuple = ()) -> Union[Exception, None]:
        with get_connector(self._config) as cnx:
            cursor = cnx.cursor()
            try:
                cursor.execute(sql, args)
                cnx.commit()
                self.log.debug('SQL RESULT "%s" = %s', sql, cursor.rowcount)
            except Exception as exc:
                self.log.error('SQL ERROR "%s" = %s', sql, exc)
                return exc

    def query_sql(self, sql: str, args: Tuple = ()) -> Tuple[List[Tuple], Exception]:
        with get_connector(self._config) as cnx:
            cursor = cnx.cursor()
            try:
                cursor.execute(sql, args)
                result = [row for row in cursor]
                self.log.debug('SQL RESULT "%s" = %s', sql, len(result))
                return result, None
            except Exception as exc:
                self.log.error('SQL ERROR "%s" = %s', sql, exc)
                return [], exc

    def read_structure(self):
        schema, err = self.query_sql(f'show columns from `{self._table_name}`')
        if not err and isinstance(schema, list):
            self._fields = [f[0] for f in schema]
            self.log.debug('%s fields = %s', self._table_name, self._fields)

    def get_to_dict(self, id: int) -> Tuple[Exception, Dict]:
        sql = f'select * from `{self._table_name}` where {self._id_field_name}={id}'
        result, err = self.query_sql(sql)
        if not err and isinstance(result, list) and len(result) > 0:
            result = result[0]
        else:
            return result, {}
        result = self.parse_to_dict(result)
        if isinstance(result, Exception):
            return result, {}
        return None, result

    def parse_to_dict(self, row: tuple) -> Union[Exception, dict]:
        if len(row) != len(self._fields):
            return ValueError(f'Expected {len(self._fields)} fields, got {len(row)}')
        result_dict = {}
        for index, key in enumerate(self._fields):
            result_dict[key] = row[index]
        return result_dict

    def get_subdata_from_post(self, post_id: int) -> Tuple[List[Dict], Exception]:
        if isinstance(post_id, dict):
            post_id = post_id.get('post_id')
            if not post_id:
                return [], ValueError('Expected post_id field')

        sql = f'select * from `{self._table_name}` where post_id={post_id}'
        result, err = self.query_sql(sql)
        if err:
            return [], err
        result_dict = []
        for row in result:
            row_dict = self.parse_to_dict(row)
            if isinstance(row_dict, dict):
                result_dict.append(row_dict)
            else:
                return result_dict, row_dict

        return result_dict, None
