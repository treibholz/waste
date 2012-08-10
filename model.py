# -*- coding: utf-8 -*-

import web
import time
import urllib2

db = web.database(dbn='sqlite', db='waste.db')

task_where = {
    'Status' : ( '(Tasks.status >= $task_where["Status"][1] or Tasks.modified >= strftime("%s","now") - 86400 ) and Tasks.deleted = 0', 0, ),
    'Tags' : None,
}

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
    dbresult = db.select('Tags', where="name like $title and deleted=0", vars=locals()).list()
    if len(dbresult) == 0:
        add_tag(title)
        result = tag(title)
    else:
        result=dbresult[0]['id']

    return result

# }}}

def get_tasks(order='id', taskFilter=None): # {{{
    return db.select('Tasks', order=order, where=taskFilter, vars=globals())

# }}}

def get_tags(order='id'): # {{{
    return db.select('Tags', order=order, where='deleted = 0')

# }}}

def get_task_tags(taskFilter=None): # {{{
    tasklist = [ t['id'] for t in db.select('Tasks', what='id', where='deleted = 0').list() ]
    taskdict = {}
    for t in tasklist:
        taskTags = db.select('Tags', what="Name", where="id in (select tag from Tagged where task = $t and deleted = 0)", vars=locals()).list()
        taskTags = [ tag['name'] for tag in taskTags ]

        taskdict[t] = taskTags

    return taskdict

# }}}

def get_tag_tasks(): # {{{
    taglist = [ t['id'] for t in db.select('Tags', what='id', where='deleted = 0').list() ]
    tagdict = {}

    for t in taglist:
        tagTasks = db.select('Tagged', what="task", where="tag = $t and deleted = 0", vars=locals()).list()
        tagTasks = [ task['task'] for task in tagTasks]

        tagdict[t] = tagTasks

    return tagdict

# }}}

def get_task_tag_ids(t): # {{{
    taskTags = db.select(   'Tagged',
                            what = "tag",
                            where="task = $t and deleted=0",
                            vars=locals()
                        ).list()

    taskTags = [ tag['tag'] for tag in taskTags]

    return taskTags

# }}}

def get_status_list_tuple(order='Status.id'): # {{{
    statuslist = []
    result = db.select('Status', what='id, name', where='deleted=0', order=order)
    for s in result:
        statuslist.append(tuple(s.values()))
    return statuslist
# }}}

def get_tag_list_tuple(order='Tags.id'): # {{{
    taglist = []
    result = db.select('Tags', what="id,name", where="deleted=0" , order=order)
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
                where = 'ID = $TaskID',
                vars=locals())

    newTags = [ x.strip() for x in EditTaskForm.d.AddTags.split(',') ]

    oldTags = get_task_tag_ids(TaskID)

    addTags = list(set(TagIDs)  - set(oldTags))
    delTags = list(set(oldTags) - set(TagIDs))
    delTags = delTags # for vim...

    print newTags
    print oldTags

    if TagIDs != []:
        #db.delete('Tagged', where="task = %s" % TaskID )
        db.update('Tagged', where="task = $TaskID and tag in $delTags and deleted=0", modified=now(), deleted=now(), vars=locals() )

        for t in addTags:
            tag_task(TaskID, t)

    if newTags != ['']:
        for t in newTags:
            tag_task(TaskID, t)


# }}}

def update_tag(TagID, Name): # {{{
    db.update('Tags',
                name = Name,
                modified = now(),
                where = 'ID = %s' % TagID)

# }}}

def tag_task(taskID, tagName): # {{{

    if type(tagName) == type(u'string'):
        tagID = tag(tagName)
    else:
        tagID = tagName
    try:
        db.insert('Tagged',
            modified = now(),
            created = now(),
            task=taskID,
            tag=tagID)
    except:
        #evil...
        pass

# }}}

def set_status(task_ID,Status): # {{{
    try:
        status_id = int(Status)
    except:
        status_id = status(Status)

    db.update('Tasks', where='id = %s' % (task_ID,) , status=status_id, modified=now())

# }}}

def add_status(status): # {{{
    db.insert('Status', name=status, modified=now(), created=now()) 

# }}}

def add_priority(priority): # {{{
    db.insert('Priority', name=priority, modified=now(), created=now())

# }}}

def add_tag(tag): # {{{
    db.insert('Tags', name=tag, modified=now(), created=now())

# }}}

def delete_task(task_ID): # {{{
    #db.delete('Tasks', where='id = %s' % (task_ID, ))
    db.update('Tasks', where='id = $task_ID', modified=now(), deleted=now(), vars=locals())

# }}}

def delete_tag(tag_ID): # {{{
    #db.delete('Tags', where='id = %s' % (tag_ID, ))
    db.update('Tags', where='id = $tag_ID', deleted=now(), modified=now(), vars=locals())
    #db.delete('Tagged', where='task = %s' % (tag_ID, ))
    db.update('Tagged', where='task = $tag_ID', deleted=now(), modified=now(), vars=locals())

# }}}

def get_taskfilter(): # {{{
    # default is "don't show tasks that are set to done more than one day ago.
    taskfilter = '1'
    for i in task_where.values():
        if i != None:
            taskfilter = '%s AND %s' % (taskfilter, i[0],)

    return taskfilter

# }}}

def set_tag_filter(TagFilter): # {{{

    TagFilterList = [ x.strip() for x in TagFilter.split(',') ]

    taglist = []
    for tag in TagFilterList:
        try:
            taglist.append(db.select('Tags',what='id', where='name like $tag and deleted=0', vars=locals()).list()[0]['id'])
        except:
            # EVIL
            pass

    if taglist != []:
        task_where['Tags'] = ( "Tasks.id in (select task from Tagged where tag in $task_where['Tags'][1])", taglist, )
    else:
        task_where['Tags'] = None

# }}}

def get_tag_filter(): # {{{

    result = ''

    if task_where['Tags'] != None:
        for t in db.select('Tags', what='name', where='id in $task_where["Tags"][1] and deleted=0', vars=globals()):
            result += '%s, ' % t['name']

    return result
# }}}

def get_taskorder(): # {{{
    return "status desc,modified desc"

# }}}

def get_single_task(task): # {{{
        return db.select('Tasks', where="id=$task", vars=locals()).list()[0]

# }}}

def db2list(db_output): # {{{
    # There must be a better way for the following...
    db_list = []

    for i in db_output:
        i_dict={}
        for k in i:
            i_dict[k] = i[k]
        db_list.append(i_dict)

    return db_list

# }}}

# API

def api_get_tasks(order='Task.ID', taskFilter=None): # {{{

    tasks = db.select('Tasks, Status', what='Tasks.*,Status.name as State', order=order, where=taskFilter + ' and Tasks.Status=Status.ID', vars=globals()).list()

    return db2list(tasks)

# }}}

# Sync

def sync_add_remote(url): # {{{
    db.insert('Sync', remote=url, lastsync=0)

# }}}

def sync_all_remote(): # {{{
    output = ''
    for entry in db.select('Sync').list():
        url = '%s/%s' % (entry['remote'], entry['lastsync'], )
        sync_from(entry['remote'], entry['lastsync'])
        sync_to(url, entry['lastsync'])
        output = "Synchronised with: %s at %s \n" % (entry['remote'] , now())

    return output

# }}}

def sync_to(url, timestamp=0): # {{{

    data = unicode(sync_db_get(timestamp))

    urllib2.urlopen(url, data).read()

    return url

# }}}

def sync_from(remote, timestamp): # {{{
    url = '%s/%s' % (remote, timestamp, )

    data = eval(urllib2.urlopen(url).read())
    sync_db_post(data, timestamp, remote)

    return url
# }}}

def sync_db_get(timestamp): # {{{
    Tables = ('Tasks', 'Tags', 'Dependencies', 'Tagged', 'Status', 'Priority')
    result = {}

    for t in Tables:
        db_output = db.select(t, where="modified >= $timestamp", vars=locals())

        result[t] = db2list(db_output)

    return result
# }}}

def sync_db_post(data, timestamp=0, remote=False): # {{{

    conflict_dict = {}

    for table in data:
        conflict_dict[table] = []

        for line in data[table]:
            try:
                db.insert(table, **line)
            except:
                conflict_dict[table].append(line)

    solve_conflicts(conflict_dict)

    print remote
    if remote:
        print remote
        db.update('Sync', lastsync=now(), where="remote = $remote", vars=locals())

# }}}

def solve_conflicts(conflict_dict): # {{{

    # Tables with IDs
    for table in ('Tasks', 'Tags', 'Status', 'Priority'):
        for r in conflict_dict[table]:
            l = db.select(table, where="id=$r['id']", vars=locals()).list()[0]

            if r['created'] == l['created']:
                if l['modified'] < r['modified']:
                    r.pop('id')
                    db.update(table, where="id=$l['id']", vars=locals(), **r)
            else:
                db.delete(table, where='id=$r["id"]', vars=locals())
                db.insert(table, **r)
                l.pop('id')
                db.insert(table, **l)

    # Tables without IDs don't need this.

# }}}

# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
