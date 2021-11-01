from execlog.setlogs import Logger


logger = Logger(
    webhook_url='Slack webhook URL',  # Slack webhook URL  # noqa
    es_hosts=['172.0.0.1:9200'],  # log on ElasticSearch host ip and port
)


if __name__ == '__main__':
    logger.notice('test notice')
