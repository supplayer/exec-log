from configlog.setlogs import Logger


logger = Logger(
    webhook_url='Slack webhook URL',  # Slack webhook URL  # noqa
    es_host='log on ElasticSearch host ip and port',  # log on ElasticSearch host ip and port
    type_on=False,
)


if __name__ == '__main__':
    logger.notice('test notice')
