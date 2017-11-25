#!/usr/bin/python3

from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import os

class PostInstallCommand(install):
    def run(self):
        info = '''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                   !
! PLEASE READ COMMENTS IN ~/.magnet/console.sh AND  !
! CHANGE SETTINGS ACCORDING YOUR SYSTEM.            !
!                                                   !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''
        print(info)
        cmd_pipeline = "apt-get install -y python-qt4 xdotool && cp -R config %s/.magnet" % os.environ.get('HOME')
        for c in cmd_pipeline.split(' && '):
            subprocess.check_output(c.split(' '))
        install.do_egg_install(self)

setup(
    name="magnet",
    version="1.0",
    packages=find_packages(),
    install_requires=['pyyaml'],
    author="Sergii Bieliaievskyi",
    description="",
    py_modules = ['magnet'],
    entry_points={ 'console_scripts': ['magnet = magnet:main'] },
    license="Apache-2.0",
    cmdclass={'install': PostInstallCommand}
)
