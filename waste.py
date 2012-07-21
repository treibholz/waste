#!/usr/bin/python
# -*- coding: utf-8 -*-

import web
#import model

urls = (
    '/',    'Index',
    '/new',  'New',
    '/setstatus', 'SetStatus',
)

render = web.template.render('templates', base='base',)

class Index: # {{{

    form = web.form.Form(
        web.form.Textbox("NewTodo", web.form.notnull, description="New: "),
        web.form.Button('Add'),
    )

    def GET(self):
        form = self.form()

        return render.index(form)

# }}}

app = web.application(urls, globals())
if __name__ == "__main__":

    app.run()

# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
