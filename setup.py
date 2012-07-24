import os
from setuptools import setup, find_packages
import user_tags


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-user-tags",
    version=user_tags.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, tagging, ajax, user',
    author='Martin Brochhaus',
    author_email='mbrochh@gmail.com',
    url="https://github.com/bitmazk/django-user-tags",
    packages=find_packages(),
    include_package_data=True,
    tests_require=[
        'fabric',
        'factory_boy',
        'django-nose',
        'coverage',
        'django-coverage',
        'selenium',
    ],
    test_suite='user_tags.tests.runtests.runtests',
)
