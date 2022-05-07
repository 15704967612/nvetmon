import os
import gevent.monkey

gevent.monkey.patch_all()
import multiprocessing

# 服务地址（adderes:port）
bind = "0.0.0.0:23456"
# 启动进程数量
worker_connections = 2000
# workers = multiprocessing.cpu_count()
workers = 4
worker_class = 'gevent'
threads = 40
preload_app = True
reload = False
x_forwarded_for_header = 'X_FORWARDED-FOR'
# 访问日志
loglevel = 'debug'
accesslog = './logs/access.log'
errorlog = './logs/error.log'
# accesslog = '-'
# errorlog = '-'
capture_output = True
