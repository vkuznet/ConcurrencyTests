#!/usr/bin/env python

import cherrypy

class Main(object):

    def index(self):
        return "Hello from Python"
    index.exposed=True
    def das(self):
        return "Hello from Python (das)"
    das.exposed=True

cherrypy.root = Main()

if __name__ == '__main__':
   cherrypy.config.update({'server.socket_port': 8212,
       'server.socket_host': '0.0.0.0',
       'server.thread_pool': 20,
       'log.screen':False,
       'environment': 'production'})
   cherrypy.quickstart(Main(), '/')
