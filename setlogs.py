from loguru import _defaults
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.tornado import TornadoIntegration
from cmreslogging.handlers import CMRESHandler
from elasticsearch import helpers as eshelpers
import sentry_sdk
import functools
import atexit as _atexit
import sys as _sys
import notifiers
import os


def find_vcs_root(path=os.getcwd(), dirs=(".git",), default=None):
    """
    get project root path.
    :param path: scripts path
    :param dirs: save rule e.g: catch git
    :param default: if set default then save to the default absolute path
    :return: path
    """
    prev, path = None, os.path.abspath(path)
    while prev != path:
        if any(os.path.isdir(os.path.join(path, d)) for d in dirs):
            return path
        prev, path = path, os.path.abspath(os.path.join(path, os.pardir))
    return default


class CMRESHANDLER(CMRESHandler):

    def flush(self):
        """fix CMRESHandler ElasticsearchDeprecationWarning for new version ES"""
        """ Flushes the buffer into ES
        :return: None
        """
        super(CMRESHANDLER, self).flush()
        if self._timer is not None and self._timer.is_alive():
            self._timer.cancel()
        self._timer = None

        if self._buffer:
            try:
                with self._buffer_lock:
                    logs_buffer = self._buffer
                    self._buffer = []
                actions = (
                    {
                        '_index': self._index_name_func.__func__(self.es_index_name),
                        # '_type': self.es_doc_type,
                        '_source': log_record
                    }
                    for log_record in logs_buffer
                )
                eshelpers.bulk(
                    client=self.__get_es_client(),
                    actions=actions,
                    stats_only=True
                )
            except Exception as exception:
                if self.raise_on_indexing_exceptions:
                    raise exception


class _SendLog(_Logger):
    def __init__(self, core=_Core(), exception=None, depth=0, record=False,
                 lazy=False, colors=True, raw=False, capture=True, patcher=None, extra={}, **kwargs_):  # noqa
        super(_SendLog, self).__init__(core, exception, depth, record, lazy, colors, raw, capture, patcher, extra)  # noqa
        kw_args = {
            'path': f'{find_vcs_root()}/docs/logs_record/running_status',
            'es_host': '',
            'app_name': find_vcs_root().split('/')[-1],
            'env': _sys.argv[-1] if '/' not in _sys.argv[-1] else 'dev',
            'receiver': 'slack',  # slack/telegram
            'dsn': None,  # for Sentry
            'webhook_url': None,  # for Slack
            'integrations': [],  # add more func item in list, for Sentry
            'apps': True,
            'rotation': '20 MB',  # for loguru
            'retention': '10 days',  # for loguru
            'enqueue': True,  # for loguru
            'level': 'INFO',  # for loguru
            'channel': 'channel',  # for notifiers
            'token': None,  # for notifiers/Telegram
            'sentry': True,  # for debug close sentry
        }
        self.kw_args = {**kw_args, **kwargs_}  # merge dicts, if keyword value changed then update  # noqa
        self.params = None
        if self.kw_args['sentry']:
            sentry_sdk.init(dsn=self.kw_args['dsn'],
                            integrations=[CeleryIntegration(),
                                          RedisIntegration(),
                                          TornadoIntegration()
                                          ] + self.kw_args['integrations'],)

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
        full_msg = \
            f'\n<le>Display item type: {type(org_msg)}</>'\
            f'\n<yellow>***↓↓↓Display By Line↓↓↓***</>'\
            f'{notes}'\
            f'\n<yellow>***↑↑↑Display By Line↑↑↑***</>\n'
        return full_msg

    def msg(self, msg, level='INFO', *args, **kwargs):
        """
        msg display on shell and record log
        """
        self._log(level, None, False, self._options, f'✉️️ → {msg}', args, kwargs)  # noqa

    def printout(self, msg, level='INFO', *args, **kwargs):
        """
        msg only display on shell.
        """
        t_logger = _SendLog(
            core=_Core(), exception=None, depth=0, record=False,
            lazy=False, colors=True, raw=False, capture=True, patcher=None, extra={}, **kwargs)
        t_logger.add(_sys.stderr)
        t_logger._log(level, None, False, self._options, f'✉️️ → {msg}', args, kwargs)

    def app(self, msg: str):
        """
        msg send to app
        """
        if self.kw_args['receiver'] == 'slack':
            self.params = {
                'channel': self.kw_args['channel'],
                'webhook_url': self.kw_args['webhook_url']}
        elif self.kw_args['receiver'] == 'telegram':
            cha_id = notifiers.get_notifier(
                self.kw_args['receiver']
            ).updates(self.kw_args['token'])[0]['message']['from']['id']
            self.params = {
                'token': self.kw_args['token'],
                'chat_id': cha_id}
        notifier = notifiers.get_notifier(self.kw_args['receiver'])
        notifier.notify(message=f'✉️️ → {msg}', **self.params)

    def notice(self, msg: str, level='INFO', *args, **kwargs):
        """
        msg send to app and record log
        """
        self._log(level, None, False, self._options, f'✉️️ → {msg}', args, kwargs)  # noqa
        self.app(msg)

    def byline(self, msg, level='INFO', sign=None, *args, **kwargs):
        """
        display msg by line
        :param level: msg level
        e.g: TRACE(5) / DEBUG(10) / INFO(20) / SUCCESS(25) / WARNING(30) / ERROR(40) / CRITICAL(50)  # noqa
        :param msg: dict/list/str
        :param sign: if msg is str, split by sign
        """
        targe_msg = self.__iteratorshow(msg, sign)
        self._log(level, None, False, self._options, targe_msg, args, kwargs)
        return msg

    def catchline(self, func, *args, **kwargs):
        """
        diplay list or dic by line.
        :param func: func
        :return: func & str notes
        """
        @functools.wraps(func)
        def wrapper(*args_, **kw):
            msg = func(*args_, **kw)
            targe_msg = self.__iteratorshow(msg)
            self._log('INFO', None, False, self._options, targe_msg, args, kwargs)  # noqa
            return func(*args_, **kw)
        return wrapper


class Logger(_SendLog):
    def __init__(self, **kwargs_):
        """
        Args Description
        path: log save location,
        receiver: slack/telegramD
        dsn: None,  for Sentry
        webhook_url: for Slack
        integrations: [], add more func item in list, for Sentry
        apps: True, switch apps
        rotation: '20 MB', for loguru
        retention: '10 days', for loguru
        enqueue: True, for loguruno
        level: 'INFO', for loguru
        channel: 'mozat', for notifiers
        token: None, for notifiers/Telegram
        sentry: True, for debug switch sentry
        """
        super(Logger, self).__init__(**kwargs_)
        logger = _SendLog(**kwargs_)
        es_args = self.kw_args['es_host'].split(':')
        es_args = es_args if len(es_args) == 2 else [es_args[0], 9200]
        # CMRESHandler.flush = CMRESHANDLER.flush
        es_handler = CMRESHANDLER(
            hosts=[{'host': es_args[0], 'port': es_args[-1]}],
            auth_type=CMRESHandler.AuthType.NO_AUTH,
            es_index_name="python_project_log",
            es_additional_fields={'App_Name': self.kw_args['app_name'],
                                  'Environment': self.kw_args['env']},)  # noqa
        # es_handler.flush = types.MethodType(flush, es_handler)
        # Default log record setting
        self.add(
            es_handler,
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",)

        if _defaults.LOGURU_AUTOINIT and _sys.stderr:
            logger.add(_sys.stderr)
        _atexit.register(logger.remove)
