# -*- coding: utf-8 -*-

"""
    alter by: dahu
    alter on 2016-11-17
"""

import os
import sys
import traceback

from tornado import web
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.httpserver import HTTPServer

try:
    import baosteel100
except ImportError:
    import sys

_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(_root)
sys.path.append(os.path.join(_root, ".."))

from baosteel100.libs.options import config
import baosteel100.bootstrap
from baosteel100.libs.loglib import get_logger


class Application(web.Application):
    def __init__(self, type):
        from baosteel100.bootstrap.urls import get_components

        (handlers, ui_modules) = get_components(type)

        settings = dict(debug=config.debug,
                        template_path=os.path.join(os.path.dirname(__file__),
                                                   "static/www"),
                        static_path=os.path.join(os.path.dirname(__file__),
                                                 "static"),
                        login_url=config.login_url,
                        xsrf_cookies=config.xsrf_cookies,
                        cookie_secret=config.cookie_secret,
                        ui_modules=ui_modules,
                        compress_response=config.compress_response,
                        serve_traceback=config.serve_traceback
                        )

        super(Application, self).__init__(handlers, **settings)

    def reverse_api(self, request):
        """Returns a URL name for a request"""
        handlers = self._get_host_handlers(request)

        for spec in handlers:
            match = spec.regex.match(request.path)
            if match:
                return spec.name

        return None


def run_main():
    try:
        from baosteel100.libs.timerlib import run_gps_timer,run_http_timer
        logger = get_logger("bootstrap")
        http_server = HTTPServer(Application('main_apps'), max_buffer_size=config.max_buffer_size,
                                 max_body_size=config.max_body_size, max_header_size=config.max_header_size)
        http_server.bind(config.port)
        http_server.start(1)
    except:
        print(traceback.format_exc())

    print("\nserver start !")
    print("port:%s" % config.port)
    logger.debug("Server start at %s" % config.port)

    IOLoop.instance().start()


def run_ftp_start():
    from baosteel100.libs.ftplib import run_ftp
    try:
        run_ftp()
    except:
        print(traceback.format_exc())


def main():
    import concurrent.futures
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        executor.submit(run_ftp_start)
        executor.submit(run_main)


if __name__ == '__main__':
    main()


