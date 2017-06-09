import logging

logger = logging.getLogger('werkzeug')


class LiggingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        logger.info('request', extra=dict(url=environ['werkzeug.request'].url,
                                          method=environ[
                                              'werkzeug.request'].method,
                                          host=environ[
                                              'werkzeug.request'].host))
        return self.app(environ, start_response)
