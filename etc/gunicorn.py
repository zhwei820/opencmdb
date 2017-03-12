#!/usr/bin/env python
# coding=utf-8
import multiprocessing

bind = '0.0.0.0:8080'
max_requests = 10000
keepalive = 5

proc_name = 'cmdb'

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gaiohttp'

loglevel = 'info'
errorlog = '-'

x_forwarded_for_header = 'X-FORWARDED-FOR'