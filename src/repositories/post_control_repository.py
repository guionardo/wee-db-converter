import sys
from typing import List, Union

from src.config import Config
from src.repositories.base_repository import BaseRepository


class PostControlRepository(BaseRepository):

    def __init__(self, config: Config, skip_setup: bool = False):
        super().__init__(config,  '_post_control', 'post_id')
        if skip_setup:
            return
        self.create_table()
        self.update_ids()

    def create_table(self):
        self.log.info('Verifying table %s', self._table_name)
        sql = f'''CREATE TABLE IF NOT EXISTS`{self._table_name}` (
  `{self._id_field_name}` int(11) NOT NULL,
  `processed_at` timestamp NULL DEFAULT NULL,
  `reason` varchar(60) NULL DEFAULT NULL,
  PRIMARY KEY (`{self._id_field_name}`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Control table for posts migrations to MongoDB';'''
        err = self.exec_sql(sql)
        if err:
            self.log.error('Cannot create table %s', self._table_name)
            sys.exit(1)

    def update_ids(self):
        self.log.info('Updating post ids for %s', self._table_name)
        sql = f'''insert into `{self._table_name}` ({self._id_field_name})
        select {self._id_field_name} from posts where {self._id_field_name} not in (select pc.{self._id_field_name} from `{self._table_name}` pc);'''
        err = self.exec_sql(sql)
        if err:
            self.log.error('Failed to update post ids')
            sys.exit(1)

    def get_unprocessed_ids(self) -> Union[Exception, List[int]]:
        self.log.info('Getting unprocessed posts')
        sql = f'select {self._id_field_name} from `{self._table_name}` where processed_at is null'
        result, _ = self.query_sql(sql)
        if isinstance(result, list):
            result = [r[0] for r in result]

        return result

    def mark_processed(self, id: int, reason: str) -> Union[Exception, None]:
        self.log.info('Marking processed post #%s - %s', id, reason)
        sql = f'''update `{self._table_name}` set reason=%s, processed_at=CURRENT_TIMESTAMP where {self._id_field_name}=%s'''
        err = self.exec_sql(sql, (reason, id))
        return err
