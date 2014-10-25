from setuptools import setup

setup(
    name='rem',
    description='Set reminders blazing fast.',
    version='1.0.1',
    install_requires=[
        'parsedatetime'
    ],
    author='Genki Sugimoto',
    author_email='cfhoyuk.reccos.nelg@gmail.com',
    url='http://github.com/Genki-S/rem/',
    download_url='https://pypi.python.org/pypi/rem/',
    license='MIT',
    entry_points={
        'console_scripts': [
            'rem=rem:main',
        ],
    },
)
