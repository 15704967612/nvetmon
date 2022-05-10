# -*- coding: utf-8 -*-
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler as _BaseAPScheduler


# 重写APScheduler，实现上下文管理机制，小优化功能也可以不要。对于任务函数涉及数据库操作有用
class APScheduler(_BaseAPScheduler):
    def run_job(self, id, jobstore=None):
        with self.app.app_context():
            super().run_job(id=id, jobstore=jobstore)


# 定时器配置项
class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'app:timer',
            'args': '',
            'trigger': 'cron',
            'minute': "*/1"
            # 'second': "*/10"
        }
    ]

    # 线程池配置，最大20个线程
    SCHEDULER_EXECUTORS = {'default': ThreadPoolExecutor(3)}
    # 调度开关开启
    SCHEDULER_API_ENABLED = True
    # 设置容错时间为 1小时
    SCHEDULER_JOB_DEFAULTS = {
        'misfire_grace_time': 10,
        'coalesce': False,
        'max_instances': 30
    }
    # 配置时区
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'


scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))