
from setuptools import setup

setup(
    name='amazpy',
    version='1.0',
    description='A simple Amazon price tracker',
    author='Lucas Hasil',
    author_email='lucashasil@gmail.com',
    url='https://github.com/lucashasil/AmazPy',
    packages=['amazpy'],
    install_requires=[
        'tk',
        'sv_ttk',
        'requests',
        'xlsxwriter',
        'bs4'
    ],
    pyton_requires='>=3.10',
)
