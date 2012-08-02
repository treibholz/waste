# -*- coding: utf-8 -*-

import web
import time

db = web.database(dbn='sqlite', db='waste.db')

def now():
    return int(time.time())

def priority(priority):
    # dummy
    return 1000

def status(title):
    # dummy
    dbresult = db.select('Status', where="name = '%s'" % (title,)).list()
    if len(dbresult) == 0:
        add_status(title)
        result = status(title)
    else:
        result=dbresult[0]['id']

    return result

def get_tasks(order='id'):
    return db.select('Tasks', order=order)

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



# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
