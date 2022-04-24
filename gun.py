import os
import gevent.monkey

gevent.monkey.patch_all()
import multiprocessing

# 服务地址（adderes:port）
bind = "0.0.0.0:23456"
# 启动进程数量
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
threads = 20
preload_app = True
reload = True
x_forwarded_for_header = 'X_FORWARDED-FOR'
# 访问日志
loglevel = 'info'
accesslog = './logs/access.log'
errorlog = './logs/error.log'
capture_output = True
