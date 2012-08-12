#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import sys

class Client(object): # {{{
    """docstring for client"""
    def __init__(self, api_url):
        super(Client, self).__init__()
        self.api_url = api_url
        self.tasks = []
        self.task_filter = []

    def get_tasks(self):
        """docstring for get_tasks"""

        url = '%s/api/get_tasks' % (self.api_url, )
        self.tasks = eval(urllib2.urlopen(url).read())

    def get_status_list(self):
        """docstring for get_status_list"""

        url = '%s/api/get_status_list' % (self.api_url, )
        return eval(urllib2.urlopen(url).read())


    def add_task(self,title,tags=''):
        """docstring for add_task"""
        url = '%s/new' % (self.api_url, )
        data = 'title=%s&tags=%s' % (title, tags,)
        urllib2.urlopen(url, data)

    def set_status(self,task_id, Status):
        """docstring for set_status"""

        url = '%s/status' % (self.api_url, )
        data = 'TaskID=%s&Status=%s' % (task_id, Status,)
        urllib2.urlopen(url, data)

    def sync(self):
        """docstring for set_status"""

        url = '%s/syncall' % (self.api_url, )
        urllib2.urlopen(url)


# }}}

class Display(object): # {{{
    """docstring for Display"""
    def __init__(self, separator='|'):
        super(Display, self).__init__()
        self.__items = ('id', 'title', 'State', )
        self.__separator = separator

    def show_tasks(self, tasks):
        """docstring for show_tasks"""

        if len(tasks) == 0:
            print "no Tasks. Jippie!"
            return True

        items = self.__items
        template = self.__get_task_template(tasks)

        title = template % tuple( [ i.upper() for i in items ] )
        print title
        line = ''
        for i in title:
            line += '-'
        print line

        for t in tasks:
            data = []
            for i in items:
                data.append(t[i])
            print template % tuple(data)

    def __get_task_template(self,tasks): # {{{
        """docstring for get_item_sizes"""

        if len(tasks) == 0:
            return ''

        items = self.__items
        separator = self.__separator
        max_size_item = {}
        template = ''

        for i in items:
            max_size_item[i] = len(i)

        for t in tasks:
            for i in items:
                if len(unicode(t[i])) > max_size_item[i]:
                    max_size_item[i] = len(unicode(t[i]))

        for i in items:
            if tasks[0][i].__class__.__name__ != 'int':
               item_format = '-'
            else:
               item_format = '+'

            template += ' %%%s%ss %s' % (item_format, max_size_item[i], separator,)

        return template
    # }}}



    def set_filter(self, items):
        """docstring for set_filter"""
        self.__items = tuple(items)

# }}}

if __name__ == "__main__":

    api_url='http://localhost:8080'

    c = Client(api_url)

    if len(sys.argv) >1:
        command = sys.argv[1].upper()

        if command == 'ADD':
            title = sys.argv[2]

            if len(sys.argv) > 3:
                tags = sys.argv[3]
            else:
                tags = ''

            c.add_task(title, tags)
        elif command == 'SYNC':
            c.sync()

        elif command in [ status.upper() for status in c.get_status_list() ]:
            status = command
            task_id = sys.argv[2]
            c.set_status(task_id, status)


    d = Display()
    c.get_tasks()
    d.show_tasks(c.tasks)

# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
