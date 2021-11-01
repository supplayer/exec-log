import sys as _sys
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


class Conf:
    __proj_root = find_vcs_root()
    conf = {}
    conf_loguru = ConfMap(
        conf,
        local_path=f'{__proj_root}/site/logs/running_status.log',
        rotation='20 MB',
        retention='10 days',
        enqueue=True,
        level='INFO',
    )
    conf_notifiers = ConfMap(
        conf,
        receiver='slack',  # slack/telegram
        webhook_url=None,  # for Slack
        channel='mozat',  # for Slack
        token=None,  # for notifiers/Telegram
    )
    conf_CMRESHandler = ConfMap(
        conf,
        es_hosts=None,
        es_index_name=f"python_project_log",
        es_additional_fields={},
        app_name=__proj_root.split('/')[-1],
        env=_sys.argv[-1] if '/' not in _sys.argv[-1] else 'dev',
    )
