from .conf import LOG_CONFIG
import logging.config
import traceback


class ContextLogger:
    USELESS_STACK = -3

    def __init__(self, name, log_level='INFO'):
        logging.config.dictConfig(LOG_CONFIG)
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.path = '/'

    def _context(self, more=False):
        stack = traceback.extract_stack()
        (filename, line, procname, text) = stack[self.USELESS_STACK]
        filename = self._filename(filename)
        steps = [self._filename(filename) + ':' + str(line) + '#' + mod + ':' + ctx
                 for filename, line, mod, ctx in stack[:self.USELESS_STACK]]
        stack = '  '.join(steps)
        context = '  (loc ' + filename + ':' + procname + ':' + str(line) + ')'
        return context + '  (stk ' + stack + ')' if more else ''

    def _filename(self, filename):
        if self.path is not None and filename.find(self.path) > -1:
            if self.path == '/':
                return filename[filename.rfind('/') + 1:]
            else:
                filename = filename[len(self.path):]
                return filename[1:] if filename.find('/') == 0 else filename
        return filename

    def critical(self, *args):
        args = [str(elem) for elem in args]
        msg = '\t'.join(args)
        self.logger.critical(msg + self._context(True))

    def error(self, *args):
        args = [str(elem) for elem in args]
        msg = '\t'.join(args)
        self.logger.error(msg + self._context(True))

    def warning(self, *args):
        args = [str(elem) for elem in args]
        msg = '\t'.join(args)
        self.logger.warning(msg + self._context())

    def info(self, *args):
        args = [str(elem) for elem in args]
        msg = '\t'.join(args)
        self.logger.info(msg + self._context())

    def debug(self, *args):
        args = [str(elem) for elem in args]
        msg = '\t'.join(args)
        self.logger.debug(msg + self._context())