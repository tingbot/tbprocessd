from setuptools import setup

setup(
    name="tbprocessd",
    py_modules=['tbprocessd', 'tbopen', 'tbtail'],
    version='0.3',
    entry_points={'console_scripts': [
        'tbprocessd = tbprocessd:main',
        'tbopen = tbopen:main',
        'tbtail = tbtail:main',
    ]},
    install_requires=[
        'pyzmq==14.7.0',
        'requests'
    ],
)
