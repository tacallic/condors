from setuptools import setup

setup(
    name='condors',
    version='1.0.0',
    python_requires='>=3.8',
    py_modules=['condors'],
    install_requires=[
        'Click==7.0.0',
        'pandas',
        'xlrd',
        'loguru',
    ],
    entry_points={
        'console_scripts': ['condors=condors:main']
    },
)