
from setuptools import setup, find_packages

setup(
    name='amazpy',
    version='1.0',
    description='A simple Amazon price tracker',
    author='Lucas Hasil',
    author_email='lucashasil@gmail.com',
    url='https://github.com/lucashasil/AmazPy',
    packages=find_packages(include=['amazpy', 'amazpy.*']),
    install_requires=[
        'tk',
        'sv_ttk',
        'requests',
        'xlsxwriter',
        'bs4'
    ],
    python_requires='>=3.10',
    entry_points={
        'amazpy': ['amazpy=amazpy.main:main']
    }
)
