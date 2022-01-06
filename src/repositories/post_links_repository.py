from typing import Dict, List, Tuple
from src.config import Config
from src.repositories.base_repository import BaseRepository


class PostLinksRepository(BaseRepository):

    def __init__(self, config: Config) -> None:
        super().__init__(config, 'post_links', 'link_id')

    def get_links_from_post(self, post_id: int) -> Tuple[List[Dict], Exception]:
        return self.get_subdata_from_post(post_id)
