#!/usr/bin/env python

from setuptools import setup

from lobster.util import get_version

setup(
    name='Lobster',
    version=get_version(),
    description='Opportunistic HEP computing tool',
    author='Anna Woodard, Matthias Wolf',
    url='https://github.com/matz-e/lobster',
    packages=[
        'lobster',
        'lobster.cmssw',
        'lobster.core',
        'lobster.commands',
        'lobster.monitor',
        'lobster.WMCore',
    ],
    package_data={'lobster': [
        'core/data/autosense.sh',
        'core/data/task.py',
        'core/data/wrapper.sh',
        'core/data/mtab',
        'core/data/siteconf/JobConfig/site-local-config.xml',
        'core/data/siteconf/PhEDEx/storage.xml',
        'core/data/merge_cfg.py',
        'core/data/merge_reports.py',
        'core/data/report.json.in',
        'commands/data/index.html',
        'commands/data/gh.png',
        'commands/data/styles.css',
        'commands/data/category.html',
    ]},
    install_requires=[
        #'httplib2',  # actually a WMCore dependency
        #'python-cjson',  # actually a DBS dependency
        #'wmcore==1.1.1rc7'  # wmcore has deps we can't resolve, so we're adding the needed classes to lobster
    ],
    entry_points={
        'console_scripts': ['lobster = lobster.ui:boil']
    }
)
