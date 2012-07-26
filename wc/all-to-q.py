#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from google.appengine.api.labs import taskqueue

for i in range(7):
    taskqueue.add(url='/one-day', params={'dayI': i}, countdown= i)
    logging.info('Adding day '+str(i)+' to the Task Queue.')
