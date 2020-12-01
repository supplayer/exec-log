from setlogs import Logger


logger = Logger(
    dsn='Your Sentry URL',  # Sentry dsn URL
    webhook_url='Your Slack webhook URL',  # Slack webhook URL  # noqa
    es_host='172.0.0.1:9200',  # log on ElasticSearch host ip and port
)


if __name__ == '__main__':
    logger.printout('test')
