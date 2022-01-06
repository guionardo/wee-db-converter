from src.config import Config
from src.repositories.base_repository import BaseRepository


class PostMediaRepository(BaseRepository):

    def __init__(self, config: Config) -> None:
        super().__init__(config, 'posts_media', 'media_id')
