import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loguru-notification",
    version="0.0.3",
    author="RoyXing",
    author_email="x254724521@hotmail.com",
    description="Project logging printout",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supplayer/loguru-notification",
    packages=setuptools.find_packages(exclude=('tests', 'requirements.txt')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'amqp==5.0.2',
        'attrs==20.3.0',
        'billiard==3.6.3.0',
        'celery==5.0.2',
        'certifi==2020.11.8',
        'chardet==3.0.4',
        'click==7.1.2',
        'click-didyoumean==0.0.3',
        'click-repl==0.1.6',
        'CMRESHandler2==2.0.4',
        'elasticsearch==7.10.0',
        'idna==2.10',
        'jsonschema==3.2.0',
        'kombu==5.0.2',
        'loguru==0.5.3',
        'notifiers==1.2.1',
        'prompt-toolkit==3.0.8',
        'pyrsistent==0.17.3',
        'pytz==2020.4',
        'redis==3.5.3',
        'requests==2.25.0',
        'rfc3987==1.3.8',
        'sentry-sdk==0.19.4',
        'six==1.15.0',
        'tornado==6.1',
        'urllib3==1.26.2',
        'vine==5.0.0',
        'wcwidth==0.2.5'
        ]
)
