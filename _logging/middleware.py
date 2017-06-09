import logging

logger = logging.getLogger('werkzeug')


class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        logger.info('request', extra=dict(url=environ['werkzeug.request'].url,
                                          method=environ[
                                              'werkzeug.request'].method,
                                          host=environ[
                                              'werkzeug.request'].host,
                                          user_ip=environ[
                                              'REMOTE_ADDR']))
        return self.app(environ, start_response)
