from setuptools import setup

setup(
    name='zzzcron',
    version='0.1',
    py_modules=['zzzc'],
    install_requires=[
        'Click',
	'PlyPlus',
	'ply'
    ],
    entry_points='''
        [console_scripts]
        zzzcron=zzzc:zzzc_run
    ''',
)
