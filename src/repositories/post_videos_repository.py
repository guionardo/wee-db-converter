from src.config import Config
from src.repositories.base_repository import BaseRepository


class PostVideosRepository(BaseRepository):

    def __init__(self, config: Config) -> None:
        super().__init__(config, 'posts_videos', 'video_id')
