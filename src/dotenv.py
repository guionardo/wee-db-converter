import logging
import os


def load_env(env_file='.env'):
    logger = logging.getLogger(__name__)
    if not env_file:
        logger.debug('nothing to load')
        return
    if not os.path.isfile(env_file):
        logger.debug('env file not found: %s', env_file)
        return
    envs = {}
    with open(env_file) as file:
        for line in file.readlines():
            line = line.strip('\n\r ')
            if not line.startswith('#') and '=' in line:
                key, value = line.split('=', maxsplit=1)
                envs[key] = value
    os.environ.update(envs)
    logging.getLogger(__name__).debug('load_env(%s)=%s', env_file, envs)
