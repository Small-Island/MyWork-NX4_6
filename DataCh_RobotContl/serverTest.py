#!/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import signal
import logging
import os
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.websocket
import time
#import sentFromJetson
cl=[]
degree = 0.0
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        if self not in cl:
            cl.append(self)
    def on_message(self, message):
        #ここにデータが来ます
        logging.info(message)
        degree = float(message)
        try:
            pass
            #sentFromJetson.writeIC2(degree)
        except:
            logging.info("I2C Error")
    def on_close(self):
        if self in cl:
            cl.remove(self)
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        body = self.get_argument('data') #index.html textarea name="body"

        len_body = len(body)
        print(len_body)
class MyApplication(tornado.web.Application):
    is_closing = False

    def signal_handler(self, signum, frame):
        logging.info('exiting...')
        self.is_closing = True

    def try_exit(self):
        if self.is_closing:
            # clean up here
            tornado.ioloop.IOLoop.instance().stop()
            logging.info('exit success')
BASE_DIR = os.path.dirname(__file__)
application = MyApplication([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
],
    template_path=os.path.join(BASE_DIR,  "templates"),
    static_path=os.path.join(BASE_DIR,  "static"),
)

def startServer():
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, application.signal_handler)
    application.listen(8888)
    tornado.ioloop.PeriodicCallback(application.try_exit, 100).start()
    tornado.ioloop.IOLoop.instance().start()   

