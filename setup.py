from setuptools import setup

setup(
    name='Azure Log Analytics Alerts',
    version='0.1',
    py_modules=['azure_log_analytics'],
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
