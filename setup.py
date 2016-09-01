from setuptools import setup

setup(
    name="tbprocessd",
    py_modules=['tbprocessd', 'tbopen', 'tbtail', 'tbbuttonsd'],
    version='0.6.0',
    entry_points={'console_scripts': [
        'tbprocessd = tbprocessd:main',
        'tbopen = tbopen:main',
        'tbtail = tbtail:main',
        'tbbuttonsd = tbbuttonsd:main',
    ]},
    install_requires=[
        'pyzmq>=14.4.0',
        'requests',
        'tingbot-python>=0.4.1',
    ],
)
