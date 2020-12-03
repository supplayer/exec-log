# loguru-notification

loguru-notification 是一个日志输出项目，在loguru的基础集成日志输出到控制台、输出到Slack、并结合CMRESHandler把日记记录到ElasticSearch，
更容易的对日志进行分析。

## Installation

1.使用python包管理工具[pip](https://pypi.org/project/loguru-notification/) 进行安装。

```bash
pip install loguru-notification
```

## Usage
对loguru-notification进行配置，并输出日志信息。

```python
from configlog.setlogs import Logger

logger = Logger(
    dsn='Your Sentry URL',  # Sentry dsn URL
    webhook_url='Your Slack webhook URL',  # Slack webhook URL  # noqa
    es_host='172.0.0.1:9200',  # log on ElasticSearch host ip and port
)

if __name__ == '__main__':
    logger.printout('输出到控制台')
    logger.msg('输出到控制台，并写入ElasticSearch')
    logger.notice('输出到控制台和Slack，并写入ElasticSearch')
```
## Contributing
欢迎使用，如果有好的优化方法也欢迎提交修改。

使用前请做适当的测试，以确定跟您的项目完全兼容。

## License
[MIT](https://choosealicense.com/licenses/mit/)