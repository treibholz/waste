#!/usr/bin/python
# -*- coding: utf-8 -*-

import web
import model

urls = (
    '/',                'Index',
    '/new',             'New',
    '/status',          'Status',
    '/filter',          'Filter',
    '/delete',          'Delete',
    '/edit/(\d*)',      'Edit',
    '/files/(.*)',      'Files',
    '/tags',            'Tags',
    '/tags/delete',     'Tags_delete',
    '/tags/update',     'Tags_update',
    '/favicon.ico',     'Favicon',
    '/api/(.*)',        'Api',
)

render = web.template.render('templates', base='base',)

class Index: # {{{

    NewTaskForm = web.form.Form(
        web.form.Textbox("title", web.form.notnull, description="New: ", placeholder="Add a new Task"),
        web.form.Textbox("tags", description='', placeholder="Tag, comma, ..."),
        web.form.Button('Add'),
    )

    DeleteTaskForm = web.form.Form(
        web.form.Button('TaskID', html='Delete'),
    )

    StatusTaskForm = web.form.Form(
        web.form.Hidden('TaskID'),
        web.form.Dropdown('Status', args=(), description=''),
    )
    DoneTaskForm = web.form.Form(
        web.form.Hidden('TaskID'),
        web.form.Button('Status', value=-1, html='Done'),
    )

    FilterForm = web.form.Form(
        web.form.Textbox("TagFilter", description="", placeholder="Tag1, tag2, ..."),
        web.form.Button("AddTagFilter", html='Filter'),
        web.form.Button("ClearTagFilter", html='Clear', value=True),
    )

    def GET(self):
        NewTaskForm = self.NewTaskForm()
        DeleteTaskForm = self.DeleteTaskForm()
        StatusTaskForm = self.StatusTaskForm()
        DoneTaskForm = self.DoneTaskForm()
        FilterForm = self.FilterForm()

        Tasks = model.get_tasks(model.get_taskorder(), model.get_taskfilter())
        Tags  = model.get_task_tags(model.get_taskfilter())

        StatusTaskForm.Status.args      =   model.get_status_list_tuple()
        FilterForm.TagFilter.value      =   model.get_tag_filter()

        return render.index(
            NewTaskForm,
            DeleteTaskForm,
            StatusTaskForm,
            DoneTaskForm,
            FilterForm,
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
        web.form.Textbox("Title", web.form.notnull, description="Title: "),
        web.form.Dropdown('Tags', args=(), description='Tags: ', multiple=True),
        web.form.Textbox("AddTags", description="Add Tags: "),
        web.form.Dropdown('Status', args=(), description='Status: '),
        web.form.Button('Save'),
        web.form.Button('Cancel', value=True),
    )

    def GET(self, task):
        taskData = model.get_single_task(task)
        taskTags = model.get_task_tag_ids(task)

        EditTaskForm = self.EditTaskForm()

        EditTaskForm.Title.set_value(taskData['title'])
        EditTaskForm.Tags.set_value(taskTags)
        EditTaskForm.Status.set_value(taskData['status'])
        # to get the new Arguments.
        EditTaskForm.Tags.args=model.get_tag_list_tuple()
        EditTaskForm.Status.args=model.get_status_list_tuple()

        return render.edit(EditTaskForm)

    def POST(self, task):
        data = web.webapi.data()
        editTags = [int(i.split('=')[1]) for i in  data.split('&') if i.split('=')[0] == 'Tags']

        EditTaskForm = self.EditTaskForm()

        if EditTaskForm.validates() and not EditTaskForm.d.Cancel:
            model.update_task(task, EditTaskForm, editTags)

        raise web.seeother('/')

# }}}

class Tags: # {{{

    DeleteTagForm = web.form.Form(
        web.form.Button('TagID', html='Delete'),
    )

    EditTagForm = web.form.Form(
        web.form.Textbox("Name", web.form.notnull, description=''),
        web.form.Hidden('TagID'),
    )

    def GET(self):
        DeleteTagForm   = self.DeleteTagForm()
        EditTagForm     = self.EditTagForm()

        usedTags        = model.get_tag_tasks()
        Tags            = model.get_tags()

        return render.tags(
            Tags,
            DeleteTagForm,
            EditTagForm,
            usedTags)

# }}}

class Tags_delete: # {{{

    def POST(self):
        DeleteTagForm = Tags.DeleteTagForm()

        if DeleteTagForm.validates():
            model.delete_tag(DeleteTagForm.d.TagID)

        raise web.seeother('/tags')

# }}}

class Tags_update: # {{{

    def POST(self):
        EditTagForm = Tags.EditTagForm()

        if EditTagForm.validates():
            model.update_tag(EditTagForm.d.TagID, EditTagForm.d.Name)

        raise web.seeother('/tags')

# }}}

class Filter: # {{{

    def POST(self):
        FilterForm = Index.FilterForm()

        if FilterForm.validates():
            if FilterForm.d.ClearTagFilter:
                model.set_tag_filter('')
            else:
                model.set_tag_filter(FilterForm.d.TagFilter)

        raise web.seeother('/')

# }}}

class Favicon: # {{{

    def GET(self):
        return open('files/favicon.ico' ).read()
# }}}

class Api:

    def GET(self, call):

        if call.lower() == 'get_tasks':
            return model.api_get_tasks(model.get_taskorder(), model.get_taskfilter())

        if call.lower() == 'get_status_list':
            status_list = [s[1] for s in model.get_status_list_tuple()]
            return status_list

app = web.application(urls, globals())
if __name__ == "__main__":

    app.run()

# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
