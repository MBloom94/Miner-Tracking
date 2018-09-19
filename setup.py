from setuptools import setup

setup(
    name = 'Miner',
    version = '0.1',
    packages = ['Miner'],
    entry_points = {
        'console_scripts': [
            'Miner = Miner.cli:main'
        ]
    })
