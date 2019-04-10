import os
import sys
from shutil import rmtree
from setuptools import setup, Command


# Meta-data
NAME = 'twitterpeel'
VERSION = '0.1.0'
DESCRIPTION = 'Twitter frontend API scraper'
AUTHOR = 'Kyle Weeks'
EMAIL = 'kylepw@gmail.com'
URL = 'https://github.com/kylepw/twitterpeel'

REQUIRED = [
    'BeautifulSoup4',
    'lxml',
    'requests',
]

HERE = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    '''Enable setup.py upload.

    Note:
        `twine` required.

    '''
    description = 'Build and publish package.'
    user_options = []

    @staticmethod
    def status(s):
        '''Print text in bold.'''
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building source and wheel distribution...')
        os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))

        self.status('Uploading package to PyPi via Twine...')
        os.system('twine upload dist/*')

        sys.exit()


with open('README.rst', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license='MIT License',
    py_modules=['twitterpeel'],
    test_suite='tests',
    install_requires=REQUIRED,
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    # Publish support
    cmdclass={
        'upload': UploadCommand,
    },
)
