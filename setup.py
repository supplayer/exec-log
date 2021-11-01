import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="exec-log",
    author="Supplayer",
    author_email="x254724521@hotmail.com",
    description="Project logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supplayer/exec-log",
    packages=setuptools.find_packages(include=('execlog',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['loguru', 'CMRESHandler2', 'notifiers'],
    setup_requires=['setuptools_scm'],
    use_scm_version=True
)
