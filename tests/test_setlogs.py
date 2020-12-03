from configlog.setlogs import Logger


logger = Logger(
    dsn='Sentry dsn URL',  # Sentry dsn URL
    webhook_url='Slack webhook URL',  # Slack webhook URL  # noqa
    es_host='log on ElasticSearch host ip and port',  # log on ElasticSearch host ip and port
    type_on=False,
    # channel='mozat'
)


if __name__ == '__main__':
    logger.notice('test notice')
