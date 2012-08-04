# -*- coding: utf-8 -*-

import web
import time

db = web.database(dbn='sqlite', db='waste.db')

def now():
    return int(time.time())

def priority(title):
    dbresult = db.select('Priority', where="name = '%s'" % (title,)).list()
    if len(dbresult) == 0:
        add_priority(title)
        result = priority(title)
    else:
        result=dbresult[0]['id']

    return result


def status(title):
    dbresult = db.select('Status', where="name = '%s'" % (title,)).list()
    if len(dbresult) == 0:
        add_status(title)
        result = status(title)
    else:
        result=dbresult[0]['id']

    return result

def get_tasks(order='id', taskFilter=None):
    return db.select('Tasks', order=order, where=taskFilter)

def get_status_list_tuple(order='id'):
    statuslist = []
    result = db.select('Status', order=order)
    for s in result:
        statuslist.append(tuple(s.values()))
    return statuslist


def new_task(text):
    db.insert('Tasks',
        title=text,
        created=now(),
        modified=now(),
        priority=priority('normal'),
        status=status('new'),
        due=None)

def set_status(task_ID,status):
    db.update('Tasks', where='id = %s' % (task_ID,) , status=int(status), modified=now())

def add_status(status):
    db.insert('Status', name=status)

def add_priority(status):
    db.insert('Priority', name=status)


def delete_task(task_ID):
    db.delete('Tasks', where='id = %s' % (task_ID, ))

def get_taskfilter():
    # default is "don't show tasks that are set to done more than one day ago.
    return "status >= 0 or modified >= %s" % (now() - 86400,)

def get_taskorder():
    return "status desc,modified"


# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
