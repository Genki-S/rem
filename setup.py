from setuptools import setup, find_packages

setup(
    name='rem',
    description='Set reminders blazing fast.',
    version='1.0.2',
    install_requires=[
        'parsedatetime'
    ],
    packages=find_packages(),
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
