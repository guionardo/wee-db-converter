from functools import lru_cache

from src.config import Config
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self, config: Config) -> None:
        super().__init__(config, 'users', 'user_id')

    @lru_cache
    def is_valid_user(self, id: int) -> bool:
        err, user = self.get_to_dict(id)
        if err or not user:
            return False
        return str(user.get('user_banned', 0)) == '0' and \
            str(user.get('user_activated', 0)) == '1'
