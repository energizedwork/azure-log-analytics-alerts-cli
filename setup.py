from setuptools import setup, find_packages
from version import __version__

setup(
    name='Azure Log Analytics Alerts',
    version=__version__,
    packages=find_packages(),
    py_modules=['cli','version'],
    install_requires=[
        'click',
        'azure-mgmt-loganalytics==0.1.0',
        'requests==2.18.4'
    ],
    entry_points='''
        [console_scripts]
        az-la-cli=cli:cli
    ''',
)
