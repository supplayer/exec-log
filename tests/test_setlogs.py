from setlogs import Logger


logger = Logger(
    dsn='http://eb01cb3614f4465793a0ec91664bc728@172.28.10.39:9000/2',  # for mozat_logs Sentry
    webhook_url='https://hooks.slack.com/services/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',  # for Mozat_logs Slack  # noqa
    es_host='172.28.10.49:9200',
)


if __name__ == '__main__':
    logger.info('eee')
