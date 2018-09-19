from setuptools import setup

setup(
    name = 'Tracker',
    version = '0.1',
    packages = ['Tracker'],
    entry_points = {
        'console_scripts': [
            'Tracker = Tracker.cli:main'
        ]
    })
