import os


class Config:
    db_host = '127.0.0.1'
    db_port = 3306
    db_user = 'root'
    db_password = 'root'
    db_name = 'video'

    redis_host = '127.0.0.1'
    redis_port = 6379
    redis_db = 3
    redis_prefix = 'video_'
    expired_seconds = 3600

    logger_directory = os.path.join(os.path.dirname(__file__), 'log')

    api_encrypt = False

