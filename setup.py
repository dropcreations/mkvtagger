from setuptools import setup, find_packages

setup(
    name='mkvtagger',
    version='0.0.0',
    author='dropcreations',
    author_email='dinitharwijesinghe@gmail.com',
    url='https://github.com/dropcreations/MKV_Tagger',
    license='MIT',
    description='Tag MKV/WebM files',
    long_description=open('README.md', 'r').read(),
    packages=find_packages(),
    install_requires=[
        'xmlformatter',
    ],
    entry_points='''
    [console_scripts]
    mkvtagger=mkvtagger:main
    '''
)
