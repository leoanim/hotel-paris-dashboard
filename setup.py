from setuptools import setup, find_packages

setup(
    name="hotel-paris-dashboard",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'dash',
        'dash-bootstrap-components',
        'pandas',
        'plotly',
        'gunicorn'
    ],
) 