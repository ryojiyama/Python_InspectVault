from setuptools import setup, find_packages

setup(
    name="toyo-safety-qc",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'openpyxl',
        'numpy',
    ],
    package_data={
        'src': ['templates/*.xlsm'],
    },
    entry_points={
        'console_scripts': [
            'csvimport=src.csvimport:main',
            'csvpivot=src.csvpivot:main',
            'csvtoxlsx=src.csvtoxlsxconverter:main',
        ],
    },
)
