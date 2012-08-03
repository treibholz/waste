#!/usr/bin/python
# -*- coding: utf-8 -*-

import web
import model

urls = (
    '/',            'Index',
    '/new',         'New',
    '/status',      'Status',
    '/delete',      'Delete',
    '/edit',        'Edit',
    '/files/(.*)',  'Files',
)



render = web.template.render('templates', base='base',)

class Index: # {{{

    NewTaskForm = web.form.Form(
        web.form.Textbox("title", description="New: "),
 #       web.form.Button('Add'),
    )

    DeleteTaskForm = web.form.Form(
        web.form.Button('TaskID', html='Delete'),
    )

    StatusTaskForm = web.form.Form(
        web.form.Hidden('TaskID'),
        web.form.Dropdown('Status', args=model.get_status_list_tuple(), description=''),
    )

    def GET(self):
        NewTaskForm = self.NewTaskForm()
        DeleteTaskForm = self.DeleteTaskForm()
        StatusTaskForm = self.StatusTaskForm()
        Tasks = model.get_tasks(model.get_taskorder(), model.get_taskfilter())
        return render.index(NewTaskForm, DeleteTaskForm, StatusTaskForm, Tasks)

# }}}

class New: # {{{

    def POST(self):
        NewTaskForm = Index.NewTaskForm()

        if NewTaskForm.validates():
            model.new_task(NewTaskForm.d.title)

        raise web.seeother('/')

# }}}

class Delete: # {{{

    def POST(self):
        DeleteTaskForm = Index.DeleteTaskForm()

        if DeleteTaskForm.validates():
            model.delete_task(DeleteTaskForm.d.TaskID)

        raise web.seeother('/')

# }}}

class Status: # {{{

    def POST(self):
        StatusTaskForm = Index.StatusTaskForm()

        if StatusTaskForm.validates():
            model.set_status(StatusTaskForm.d.TaskID, StatusTaskForm.d.Status)

        raise web.seeother('/')

# }}}

class Files: # {{{

    def GET(self,filename):
        return open('files/%s' % (filename,) ).read()

# }}}



app = web.application(urls, globals())
if __name__ == "__main__":

    app.run()

# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
