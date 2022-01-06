import logging
from typing import Dict, Tuple

from src.repositories.base_output_repository import BaseOutputRepository
from src.repositories.post_control_repository import PostControlRepository
from src.repositories.post_links_repository import PostLinksRepository
from src.repositories.post_media_repository import PostMediaRepository
from src.repositories.post_photos_repository import PostPhotosRepository
from src.repositories.post_repository import PostRepository
from src.repositories.post_videos_repository import PostVideosRepository
from src.repositories.user_repository import UserRepository


class PostsService:

    def __init__(self, output: BaseOutputRepository,
                 post_control: PostControlRepository,
                 posts: PostRepository,
                 post_photos: PostPhotosRepository,
                 post_links: PostLinksRepository,
                 post_media: PostMediaRepository,
                 post_videos: PostVideosRepository,
                 users: UserRepository):
        self.log = logging.getLogger(__name__)
        self._ouput = output
        self._control = post_control
        self._posts = posts
        self._post_photos = post_photos
        self._post_links = post_links
        self._post_media = post_media
        self._post_videos = post_videos
        self._users = users

    def run(self):
        unprocessed = self._control.get_unprocessed_ids()
        if not isinstance(unprocessed, list):
            self.log.error('Cannot run posts service: %s', unprocessed)
            return
        if len(unprocessed) == 0:
            self.log.info('There are no posts to process')
            return

        for id in unprocessed:
            self.process(id)

    def process(self, id: int):
        err, post = self._posts.get_to_dict(id)
        if err:
            self.log.error('Ignoring post #%s - %s', id, err)
            return

        user_type = str(post.get('user_type', None) or '').lower()
        if not user_type or user_type not in ['page', 'user']:
            self.log.error('Invalid post #%s - USER_TYPE')
            self._control.mark_processed(id, 'INVALID USER_TYPE')
            return

        if user_type == 'user':
            user_id = post.get('user_id', 0)
            if not self._users.is_valid_user(user_id):
                self.log.warning(
                    'Ignoring post #%s - user #%s is not valid', id, user_id)
                self._control.mark_processed(id, f'INVALID USER {user_id}')
                return

        post_type = str(post.get('post_type', None) or '').lower()
        sub_process_method = {
            'photos': self.process_photos,
            'group_picture': self.process_photos,
            'page_cover': self.process_photos,
            'page_picture': self.process_photos,
            'profile_cover': self.process_photos,
            'profile_picture': self.process_photos,
            'link': self.process_links,
            'media': self.process_media,
            'video': self.process_videos,
            '': self.process_dummy}.get(post_type, None)

        if not sub_process_method:
            self.log.error('Invalid post #%s - POST_TYPE')
            self._control.mark_processed(id, 'INVALID POST_TYPE')
            return

        if post_type:
            sub_process_data, err = sub_process_method(post)
            if not err:
                post[post_type+'s'] = sub_process_data
            else:
                self.log.error('Error processing ')

        error = self._ouput.save(id, post)
        if not error:
            self._control.mark_processed(id, 'SAVED')
            self.log.info('Processed post #%s', id)
        else:
            self.log.error('Failed to process post #%s - %s', id, error)

    def process_photos(self, post: dict) -> Tuple[Dict, Exception]:
        return self._post_photos.get_subdata_from_post(post)

    def process_links(self, post: dict) -> Tuple[Dict, Exception]:
        return self._post_links.get_subdata_from_post(post)

    def process_media(self, post: dict) -> Tuple[Dict, Exception]:
        return self._post_media.get_subdata_from_post(post)

    def process_videos(self, post: dict) -> Tuple[Dict, Exception]:
        return self._post_videos.get_subdata_from_post(post)

    def process_dummy(self, post: dict) -> Tuple[Dict, Exception]:
        return None, None

    def set_processed(self, id: int, reason: str):
        ...
