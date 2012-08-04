# -*- coding: utf-8 -*-

import web
import time

db = web.database(dbn='sqlite', db='waste.db')

def now(): # {{{
    return int(time.time())
# }}}

def priority(title): # {{{
    dbresult = db.select('Priority', where="name like '%s'" % (title,)).list()
    if len(dbresult) == 0:
        add_priority(title)
        result = priority(title)
    else:
        result=dbresult[0]['id']

    return result
# }}}

def status(title): # {{{
    dbresult = db.select('Status', where="name like '%s'" % (title,)).list()
    if len(dbresult) == 0:
        add_status(title)
        result = status(title)
    else:
        result=dbresult[0]['id']

    return result

# }}}

def tag(title): # {{{
    dbresult = db.select('Tags', where="name like '%s'" % (title,)).list()
    if len(dbresult) == 0:
        add_tag(title)
        result = tag(title)
    else:
        result=dbresult[0]['id']

    return result

# }}}

def get_tasks(order='id', taskFilter=None): # {{{
    return db.select('Tasks', order=order, where=taskFilter)

# }}}

def get_task_tags(taskFilter=None): # {{{
    tasklist = [ t['id'] for t in db.select('Tasks',what='id').list() ]
    taskdict = {}
    for t in tasklist:
        taskTags = db.select('Tags', what="Name", where="id in (select tag from Tagged where task = %s )" % (t,)).list()
        taskTags = [ tag['name'] for tag in taskTags] 

        taskdict[t] = taskTags

    return taskdict

# }}}

def get_task_tag_ids(t): # {{{
    taskTags = db.select('Tagged', what = "tag", where="task = %s " % (t,)).list()
    taskTags = [ tag['tag'] for tag in taskTags] 

    return taskTags

# }}}

def get_status_list_tuple(order='id'): # {{{
    statuslist = []
    result = db.select('Status', order=order)
    for s in result:
        statuslist.append(tuple(s.values()))
    return statuslist
# }}}

def get_tag_list_tuple(order='id'): # {{{
    taglist = []
    result = db.select('Tags', order=order)
    for s in result:
        taglist.append(tuple(s.values()))
    return taglist
# }}}

def new_task(text, tags): # {{{

    tags = [ x.strip() for x in tags.split(',') ]

    taskID = db.insert('Tasks',
                title=text,
                created=now(),
                modified=now(),
                priority=priority('normal'),
                status=status('new'),
                due=None)

    if tags != ['']:
        for t in tags:
            tag_task(taskID, t)

# }}}

def update_task(TaskID, EditTaskForm, TagIDs): # {{{
    db.update('Tasks',
                title = EditTaskForm.d.Title,
                modified = now(),
                status = EditTaskForm.d.Status,
                where = 'ID = %s' % TaskID)

    newTags = [ x.strip() for x in EditTaskForm.d.AddTags.split(',') ]

    if TagIDs != []:
        db.delete('Tagged', where="task = %s" % TaskID )
        for t in TagIDs:
            tag_task(TaskID, t)

    if newTags != ['']:
        for t in newTags:
            tag_task(TaskID, t)


# }}}

def tag_task(taskID, tagName): # {{{

    if type(tagName) == type('string'):
        tagID = tag(tagName)
    else:
        tagID = tagName

    db.insert('Tagged',
        task=taskID,
        tag=tagID)

# }}}

def set_status(task_ID,status): # {{{
    db.update('Tasks', where='id = %s' % (task_ID,) , status=int(status), modified=now())

# }}}

def add_status(status): # {{{
    db.insert('Status', name=status)

# }}}

def add_priority(priority): # {{{
    db.insert('Priority', name=priority)

# }}}

def add_tag(tag): # {{{
    db.insert('Tags', name=tag)

# }}}

def delete_task(task_ID): # {{{
    db.delete('Tasks', where='id = %s' % (task_ID, ))

# }}}

def get_taskfilter(): # {{{
    # default is "don't show tasks that are set to done more than one day ago.
    return "status >= 0 or modified >= %s" % (now() - 86400,)

# }}}

def get_taskorder(): # {{{
    return "status desc,modified"

# }}}

def get_single_task(task): # {{{
        return db.select('Tasks', where="id=%s" % task).list()[0]

# }}}

# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
