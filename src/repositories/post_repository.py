from src.config import Config
from src.repositories.base_repository import BaseRepository


class PostRepository(BaseRepository):

    def __init__(self, config: Config):
        super().__init__(config, 'posts', 'post_id')
