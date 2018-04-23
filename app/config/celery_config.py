from celery.schedules import crontab


task_serializer = 'json'
result_serializer = 'json'
result_expires = 60 * 60 * 24  # 任务过期时间
accept_content = ["json"]  # 指定任务接受的内容类型.


# Timezone
timezone = 'Asia/Shanghai'
enable_utc = True

# import
include = (
    'app.tasks.info_task',
    'app.tasks.cnnvd_task',
    'app.tasks.threat_ip',
    'app.tasks.threat_domain',
    'app.tasks.get_ip_info_task'
)

# schedules
beat_schedule = {
    'info_task': {
        'task': 'app.tasks.info_task.run_info',
        'schedule': crontab(hour=1, minute=1),
        'args': ()
    },
    'cnnvd_task': {
        'task': 'app.tasks.cnnvd_task.run_cnnvd',
        'schedule': crontab(hour=1, minute=2),
        'args': ()
    },
    'threat_ip': {
        'task': 'app.tasks.threat_ip.run_ip',
        'schedule': crontab(hour=1, minute=3),
        'args': ()
    },
    'threat_domain': {
        'task': 'app.tasks.threat_domain.run_domain',
        'schedule': crontab(hour=1, minute=4),
        'args': ()
    },
    'get_ip_info': {
        'task': 'app.tasks.get_ip_info_task.get_ip_info',
        'schedule': crontab(hour=3, minute=3),
        'args': ()
    }
}
