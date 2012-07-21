# -*- coding: utf-8 -*-

import web
import time

db = web.database(dbn='sqlite', db='waste.db')

def now():
    return int(time.time())

def priority(priority):
    # dummy
    return 1000

def status(status):
    # dummy
    return 0

def get_tasks(order='id'):
    return db.select('Tasks', order=order)

def new_task(text):
    db.insert('Tasks',
        title=text,
        created=now(),
        modified=now(),
        priority=priority('normal'),
        status=status('new'),
        due=none)
        
#def set_tag(task, tag):

    

# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
