# exec-log

exec-log 是一个日志输出项目，在loguru的基础集成日志输出到控制台、输出到Slack、并结合CMRESHandler把日记记录到ElasticSearch，
更容易的对日志进行分析。

## Installation

1.使用python包管理工具 [pip](https://pypi.org/project/exec-log/) 进行安装。

```bash
pip install exec-log
```

## Usage
对exec-log进行配置，并输出日志信息。
日志分为7个级别: TRACE(5) / DEBUG(10) / INFO(20) / SUCCESS(25) / WARNING(30) / ERROR(40) / CRITICAL(50)

```python
from execlog.setlogs import Logger

logger = Logger(
    webhook_url='Your Slack webhook URL',  # Slack webhook URL  # noqa
    es_hosts=['172.0.0.1:9200'],  # 记录日期 ElasticSearch host ip and port
    # log_path=f'{proj_root}/site/logs/running_status.log' # 如果不用ElasticSearch可以自定义log保存路径或使用默认路径
)

if __name__ == '__main__':
    logger.echo('输出到控制台')
    logger.app("发送到Slack")
    logger.trace('输出到控制台，并写入ElasticSearch或本地', note='这个参数只会在ES显示，ES会添加字段名为extra.note, <<note参数名>>可以随情况更改，<<也可以不设置>>， 相应ES字段名也会动态更改。')
    logger.debug('输出到控制台，并写入ElasticSearch或本地', note='这个参数只会在ES显示，ES会添加字段名为extra.note, <<note参数名>>可以随情况更改，<<也可以不设置>>， 相应ES字段名也会动态更改。')
    logger.info('输出到控制台，并写入ElasticSearch或本地', note='这个参数只会在ES显示，ES会添加字段名为extra.note, <<note参数名>>可以随情况更改，<<也可以不设置>>， 相应ES字段名也会动态更改。')
    logger.success('输出到控制台，并写入ElasticSearch或本地', note='这个参数只会在ES显示，ES会添加字段名为extra.note, <<note参数名>>可以随情况更改，<<也可以不设置>>， 相应ES字段名也会动态更改。')
    logger.warning('输出到控制台，并写入ElasticSearch或本地', note='这个参数只会在ES显示，ES会添加字段名为extra.note, <<note参数名>>可以随情况更改，<<也可以不设置>>， 相应ES字段名也会动态更改。')
    logger.error('输出到控制台，并写入ElasticSearch或本地', note='这个参数只会在ES显示，ES会添加字段名为extra.note, <<note参数名>>可以随情况更改，<<也可以不设置>>， 相应ES字段名也会动态更改。')
    logger.critical('输出到控制台，并写入ElasticSearch或本地', note='这个参数只会在ES显示，ES会添加字段名为extra.note, <<note参数名>>可以随情况更改，<<也可以不设置>>， 相应ES字段名也会动态更改。')
    logger.notice('输出到控制台和Slack，并写入ElasticSearch或本地', level='INFO', note='这个参数只会在ES显示，ES会添加字段名为extra.note, <<note参数名>>可以随情况更改，<<也可以不设置>>， 相应ES字段名也会动态更改。')
```
## Contributing
欢迎使用，如果有好的优化方法也欢迎提交修改。

使用前请做适当的测试，以确定跟您的项目完全兼容。

## License
[MIT](https://choosealicense.com/licenses/mit/)