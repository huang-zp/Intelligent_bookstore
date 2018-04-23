import sys
from app.engines import db
from app.logger import ContextLogger
from app.utill.req import BaseReq


class Task(BaseReq):
    def __init__(self, name, time=None):
        super().__init__()
        self.logger = ContextLogger('sync_sqlite')
        self.name = name
        self.time = time

    def start(self):
        self.logger.info("Task Started: {}".format(self.name))

    def exit(self):
        sys.exit()

    def process(self):
        pass

    def finish(self):
        self.logger.info("Task Finished: {}".format(self.name))

    def safe_commit(self, value):
        try:
            db.session.add(value)
            db.session.commit()
            self.logger.info('同步成功')
        except Exception as e:
            self.logger.warning(e)
            db.session.rollback()

    def run(self):
        self.start()
        self.process()
        self.finish()



