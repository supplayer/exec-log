import sys as _sys
import os


def find_vcs_root(path=os.getcwd(), dirs=(".git",), default=''):
    """
    get project root path.
    :param path: scripts path
    :param dirs: save rule e.g: catch git
    :param default: if set default then save to the default absolute path
    :return: path
    """
    if default:
        return default
    prev, path = None, os.path.abspath(path)
    while prev != path:
        if any(os.path.isdir(os.path.join(path, d)) for d in dirs):
            return path
        prev, path = path, os.path.abspath(os.path.join(path, os.pardir))
    return default


class ConfMap:
    def __init__(self, conf: dict, **kwargs):
        self.__conf = conf
        self.__conf_app = {**kwargs}
        self.__conf.update(kwargs)

    def __getitem__(self, item):
        return self.__conf_app[item]

    @property
    def dicts(self):
        return self.__conf_app


class ConfDict(dict):
    def update_not_none(self, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v}
        self.update(kwargs)


class Conf:
    __proj_root = find_vcs_root()
    conf = ConfDict()
    conf_loguru = ConfMap(
        conf,
        log_path=f'{__proj_root}/site/logs/running_status.log',
        rotation='20 MB',
        retention='10 days',
        enqueue=True,
        level='INFO',
    )
    conf_notifiers = ConfMap(
        conf,
        receiver='slack',  # slack/telegram
        webhook_url=None,  # for Slack
        channel='default',  # for Slack
        token=None,  # for notifiers/Telegram
    )
    conf_CMRESHandler = ConfMap(
        conf,
        es_hosts=None,
        es_exclude_fields=['msg'],
        es_index_name=f"python_project_log",
        es_doc_type=None,
        es_additional_fields={},
        app_name=__proj_root.split('/')[-1],
        env=_sys.argv[-1] if '/' not in _sys.argv[-1] else 'dev',
    )
