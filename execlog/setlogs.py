from execlog.config import Conf
from execlog.tools import Modify
from loguru import _defaults
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger
from cmreslogging.handlers import CMRESHandler
import functools
import atexit as _atexit
import sys as _sys
import notifiers


class Logger(_Logger):
    def __init__(self, core=_Core(), exception=None, depth=0, record=False,
                 lazy=False, colors=True, raw=False, capture=True, patcher=None, extra=None, **kwargs):
        super(Logger, self).__init__(core, exception, depth, record, lazy, colors, raw, capture, patcher, extra or {})
        """
        Args Description
        path: log save location,
        receiver: slack/telegramD
        webhook_url: for Slack
        rotation: '20 MB', for loguru
        retention: '10 days', for loguru
        enqueue: True, for loguruno
        level: 'INFO', for loguru
        channel: 'mozat', for notifiers
        """
        self.setting = Conf()
        self.setting.conf.update(kwargs)
        self.__logger = self.__set_logger()
        self.__notifier = self.__app_notifier()
        self.add(self.__es_handler or self.setting.conf_loguru['local_path'])
        if _defaults.LOGURU_AUTOINIT and _sys.stderr:
            self.add(_sys.stderr)
        _atexit.register(self.remove)

    def echo(self, msg, level='INFO', *args, **kwargs):
        """
        msg only display on shell.
        """
        self.__logger._log(level, None, False, self._options, msg, args, kwargs)

    def app(self, msg):
        """
        msg send to app
        """
        self.__notifier[0].notify(raise_on_errors=True, message=str(msg), **self.__notifier[1])

    def notice(self, msg, level='INFO', *args, **kwargs):
        """
        msg send to app and record log
        """
        self._log(level, None, False, self._options, msg, args, kwargs)
        self.app(msg)

    def byline(self, msg, level='INFO', sign=None, log_type='echo', *args, **kwargs):
        """
        display msg by line
        :param log_type: echo
        :param level: msg level
        e.g: TRACE(5) / DEBUG(10) / INFO(20) / SUCCESS(25) / WARNING(30) / ERROR(40) / CRITICAL(50)
        :param msg: dict/list/str
        :param sign: if msg is str, split by sign
        """
        targe_msg = self.__iteratorshow(msg, sign)
        if log_type == 'echo':
            self.__logger._log(level, None, False, self._options, targe_msg, args, kwargs)
        else:
            self._log(level, None, False, self._options, targe_msg, args, kwargs)
        return msg

    def catchline(self, level='INFO', log_type='echo', *args, **kwargs):
        """
        diplay list or dic by line.
        :param log_type: echo
        :param level: msg level
        e.g: TRACE(5) / DEBUG(10) / INFO(20) / SUCCESS(25) / WARNING(30) / ERROR(40) / CRITICAL(50)
        :return: func & str notes
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args_, **kw):
                msg = func(*args_, **kw)
                targe_msg = self.__iteratorshow(msg)
                if log_type == 'echo':
                    self.__logger._log(level, None, False, self._options, targe_msg, args, kwargs)
                else:
                    self._log(level, None, False, self._options, targe_msg, args, kwargs)
                return func(*args_, **kw)
            return wrapper
        return decorator

    @staticmethod
    def __iteratorshow(msg, sign=None):
        """
        reset msg format
        :param msg: dict/list/str/tuple/set
        :param sign: if msg is str, split by sign
        :return: str
        """
        org_msg, notes = msg, ''
        if isinstance(msg, str):
            msg = msg.split(sign) if sign else f'\n{msg}'
        if isinstance(msg, dict):
            for k, v in msg.items():
                notes += f'\n<blue>{k}</>: {v}'
        elif isinstance(msg, (list, tuple, set)):
            for k, v in enumerate(msg):
                notes += f'\n<blue>{k}</> → {v}'
        else:
            notes = f"\n{msg}"
        return Modify.pretty(f'<le>Display item type: {type(org_msg)}</>\n{notes}', "Display By Line")

    def __app_notifier(self):
        if self.setting.conf['receiver'] == 'slack':
            self.params = {
                'channel': self.setting.conf['channel'],
                'webhook_url': self.setting.conf['webhook_url']}
        elif self.setting.conf['receiver'] == 'telegram':
            cha_id = notifiers.get_notifier(
                self.setting.conf['receiver']
            ).updates(self.setting.conf['token'])[0]['message']['from']['id']
            self.params = {
                'token': self.setting.conf['token'],
                'chat_id': cha_id}
        return notifiers.get_notifier(self.setting.conf['receiver']), self.params

    @staticmethod
    def __set_logger():
        l_ = _Logger(core=_Core(), exception=None, depth=0, record=False, lazy=False, colors=True,
                     raw=False, capture=True, patcher=None, extra={})
        l_.add(_sys.stderr)
        return l_

    @property
    def __es_handler(self):
        return CMRESHandler(
            hosts=[(lambda i: {'host': i[0], 'port': i[-1]})(i.split(':')) for i in self.setting.conf['es_hosts']],
            es_index_name=self.setting.conf['es_index_name'],
            es_additional_fields={**{'App_Name': self.setting.conf['app_name'],
                                     'Environment': self.setting.conf['env']},
                                  **self.setting.conf['es_additional_fields']}
        ) if self.setting.conf['es_hosts'] else None
