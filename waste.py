#!/usr/bin/python
# -*- coding: utf-8 -*-

import web
#import model

urls = (
    '/',    'Index',
    'new',  'New',
)

class Index:

    def GET(self):
        return "Dummy"


app = web.application(urls, globals())
if __name__ == "__main__":

    app.run()

# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
