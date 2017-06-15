"""Support for different operating systems.

For Qpython on Android, the current working directory is / by default."""


import platform
import os

machine = platform.machine()
print("Entering in lib_fix_os")
print('machine: ' + machine)
print(__file__)
dirname = os.path.dirname(__file__) 
print(dirname)

if (machine == 'armv7l'): # android
    print("Android OS detected")
    os.chdir(os.path.dirname(__file__))
    print(os.getcwd())
    
print("Exiting from lib_fix_os")
