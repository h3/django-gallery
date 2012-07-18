# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='django-gallery',
    version='1.1.0',
    description='Dead simple gallery.',
    author='Maxime Haineault (Motion Média)',
    author_email='max@motion-m.ca',
    url='',
    download_url='',
    packages=find_packages(),
    include_package_data=True,
    package_data={'gallery': [
        'locale/*',
        'templates/*',
        ]},
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
