from setuptools import setup, find_packages

setup(
    name="fruteria",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
    ],
) 