import os
from src.config import Config

from src.dotenv import load_env
from src.logging import setup_logging
from src.repositories.file_output_repository import FileOutputRepository
from src.repositories.mongodb_output_repository import MongoDbOutputRepository
from src.repositories.post_control_repository import PostControlRepository
from src.repositories.post_links_repository import PostLinksRepository
from src.repositories.post_media_repository import PostMediaRepository
from src.repositories.post_photos_repository import PostPhotosRepository
from src.repositories.post_repository import PostRepository
from src.repositories.post_videos_repository import PostVideosRepository
from src.repositories.user_repository import UserRepository
from src.services.posts_service import PostsService


def main():
    setup_logging()
    load_env(os.getenv('ENV_FILE', None))
    config = Config()
    post_control = PostControlRepository(config)
    users = UserRepository(config)
    posts = PostRepository(config)
    posts_photos = PostPhotosRepository(config)
    posts_links = PostLinksRepository(config)
    posts_media = PostMediaRepository(config)
    posts_video = PostVideosRepository(config)
    output = FileOutputRepository(config)
    # output = MongoDbOutputRepository(config)
    service = PostsService(output, post_control, posts,
                           posts_photos, posts_links, posts_media, posts_video,users)
    service.run()


if __name__ == '__main__':
    main()
