#!/usr/bin/python
# -*- coding: utf-8 -*-

import web
import model

urls = (
    '/',            'Index',
    '/new',         'New',
    '/status',      'Status',
    '/delete',      'Delete',
    '/edit/(\d*)',        'Edit',
    '/files/(.*)',  'Files',
)



render = web.template.render('templates', base='base',)

class Index: # {{{

    NewTaskForm = web.form.Form(
        web.form.Textbox("title", description="New: "),
        web.form.Textbox("tags", description="Tags: "),
        web.form.Button('Add'),
    )

    DeleteTaskForm = web.form.Form(
        web.form.Button('TaskID', html='Delete'),
    )

    StatusTaskForm = web.form.Form(
        web.form.Hidden('TaskID'),
        web.form.Dropdown('Status', args=model.get_status_list_tuple(), description=''),
    )
    DoneTaskForm = web.form.Form(
        web.form.Hidden('TaskID'),
        web.form.Button('Status', value=-1, html='Done'),
    )


    def GET(self):
        NewTaskForm = self.NewTaskForm()
        DeleteTaskForm = self.DeleteTaskForm()
        StatusTaskForm = self.StatusTaskForm()
        DoneTaskForm = self.DoneTaskForm()

        Tasks = model.get_tasks(model.get_taskorder(), model.get_taskfilter())
        Tags  = model.get_task_tags(model.get_taskfilter())

        return render.index(
            NewTaskForm,
            DeleteTaskForm,
            StatusTaskForm,
            DoneTaskForm,
            Tasks,
            Tags)

# }}}

class New: # {{{

    def POST(self):
        NewTaskForm = Index.NewTaskForm()

        if NewTaskForm.validates():
            model.new_task(NewTaskForm.d.title, NewTaskForm.d.tags)

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

class Edit: # {{{

    EditTaskForm = web.form.Form(
        web.form.Textbox("Title", description="Title: "),
        web.form.Dropdown('Tags', args=model.get_tag_list_tuple(), description='Tags: ', multiple=True),
        web.form.Textbox("AddTags", description="Add Tags: "),
        web.form.Dropdown('Status', args=model.get_status_list_tuple(), description='Status: '),
        web.form.Button('Save'),
        web.form.Button('Cancel'),
    )


    def GET(self, task):
        taskData = model.get_single_task(task)
        taskTags = model.get_task_tag_ids(task)

        EditTaskForm = self.EditTaskForm()

        EditTaskForm.Title.set_value(taskData['title'])
        EditTaskForm.Tags.set_value(taskTags)
        EditTaskForm.Status.set_value(taskData['status'])

        return render.edit(EditTaskForm)

    def POST(self, task):
        data = web.webapi.data()
        editTags = [int(i.split('=')[1]) for i in  data.split('&') if i.split('=')[0] == 'Tags']

        EditTaskForm = self.EditTaskForm()

        if EditTaskForm.validates():
            model.update_task(task, EditTaskForm, editTags)

        raise web.seeother('/')

# }}}



app = web.application(urls, globals())
if __name__ == "__main__":

    app.run()

# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
