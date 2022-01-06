from typing import Dict, List, Tuple

from src.config import Config
from src.repositories.base_repository import BaseRepository


class PostPhotosRepository(BaseRepository):

    def __init__(self, config: Config):
        super().__init__(config, 'posts_photos', 'photo_id')

    def get_photos_from_post(self, post_id: int) -> Tuple[List[Dict], Exception]:
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
